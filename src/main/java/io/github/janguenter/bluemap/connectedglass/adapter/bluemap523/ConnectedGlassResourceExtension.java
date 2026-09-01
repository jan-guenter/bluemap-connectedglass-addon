/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap523;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePackExtension;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.texture.Texture;
import de.bluecolored.bluemap.core.util.Key;
import de.bluecolored.bluemap.core.world.BlockProperties;
import de.bluecolored.bluemap.core.world.BlockState;
import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.SyntheticDispatch;
import io.github.janguenter.bluemap.connectedglass.activation.ConnectedGlassRuntime;
import io.github.janguenter.bluemap.connectedglass.profile.ExactModArtifactDetector;
import io.github.janguenter.bluemap.connectedglass.profile.ProfileDisablement;
import io.github.janguenter.bluemap.connectedglass.profile.ConnectedGlass1114Fusion1312Profile;
import io.github.janguenter.bluemap.connectedglass.profile.ConnectedGlassDefinition;
import io.github.janguenter.bluemap.connectedglass.profile.TextureCatalog;

import java.awt.image.BufferedImage;
import java.awt.Graphics2D;
import java.io.IOException;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.Map;
import java.util.Set;

/** Exact artifact/schema activation, tile cropping, and allowlist routing. */
final class ConnectedGlassResourceExtension implements ResourcePackExtension {

    static final Key SYNTHETIC = Key.parse("bluemap_connectedglass:fusion_model");

    private final ResourcePack resourcePack;
    private final ConnectedGlassRuntime runtime;
    private Map<TileKey, Key> tileKeys = Map.of();

    ConnectedGlassResourceExtension(ResourcePack resourcePack, ConnectedGlassRuntime runtime) {
        this.resourcePack = resourcePack;
        this.runtime = runtime;
    }

    @Override
    public void loadResources(Iterable<Path> roots) throws IOException, InterruptedException {
        try {
            loadVerifiedResources(roots);
        } catch (IOException | RuntimeException exception) {
            runtime.inactive("active-resource-read-failed");
        }
    }

    private void loadVerifiedResources(Iterable<Path> roots)
            throws IOException, InterruptedException {
        if (ProfileDisablement.current().isDisabled(
                ConnectedGlass1114Fusion1312Profile.PROFILE_ID
        )) {
            runtime.inactive("operator-disabled");
            return;
        }
        if (!ExactModArtifactDetector.matchesRequiredPair(roots)) {
            runtime.inactive("exact-artifact-pair-missing");
            return;
        }
        ActiveResourceSchemaValidator.Result schema = ActiveResourceSchemaValidator.validate(
                resourcePack,
                roots,
                ConnectedGlass1114Fusion1312Profile.RESOURCES,
                ConnectedGlass1114Fusion1312Profile.TEXTURES
        );
        if (!schema.valid()) {
            runtime.inactive(schema.reason());
            return;
        }
        if (!SyntheticDispatch.matches(
                resourcePack.getBlockStates().get(SYNTHETIC),
                BlueMap523Adapter.renderer()
        )) {
            runtime.inactive("synthetic-dispatch-invalid");
            return;
        }
        runtime.activate(schema.catalog());
    }

    @Override
    public Set<Key> collectUsedTextureKeys() {
        if (!runtime.route().isActive()) {
            return Set.of();
        }
        Set<Key> used = new LinkedHashSet<>(
                ConnectedGlass1114Fusion1312Profile.TEXTURES.keys()
        );
        used.addAll(plannedTiles().values());
        return Set.copyOf(used);
    }

    @Override
    public void bake() {
        if (!runtime.route().isActive()) {
            return;
        }
        try {
            Map<TileKey, Key> planned = plannedTiles();
            for (Key output : planned.values()) {
                if (resourcePack.getTextures().get(output) != null) {
                    runtime.inactive("synthetic-texture-collision");
                    return;
                }
            }
            Map<Key, Texture> generated = cropTiles(planned);
            if (generated.size() != planned.size()) {
                runtime.inactive("required-texture-invalid");
                return;
            }
            generated.forEach(resourcePack.getTextures()::put);
            tileKeys = Map.copyOf(planned);
        } catch (IOException | RuntimeException exception) {
            runtime.inactive("required-texture-invalid");
        }
    }

    @Override
    public Key getBlockStateKey(Key key) {
        return runtime.route().isActive()
                && ConnectedGlass1114Fusion1312Profile.ROUTED_BLOCKS.contains(key.getFormatted())
                ? SYNTHETIC : key;
    }

    @Override
    public void getBlockProperties(BlockState state, BlockProperties.Builder builder) {
        if (!runtime.route().isActive()) {
            return;
        }
        ConnectedGlassDefinition definition = ConnectedGlass1114Fusion1312Profile.DEFINITIONS.get(
                state.getId().getFormatted()
        );
        if (definition == null) {
            return;
        }
        applyProperties(state, definition, builder);
    }

    static void applyProperties(
            BlockState state,
            ConnectedGlassDefinition definition,
            BlockProperties.Builder builder
    ) {
        if (!ConnectedGlassStateSchema.accepts(state, definition)) {
            builder
                    .culling(false)
                    .occluding(false)
                    .cullingIdentical(false);
            return;
        }
        switch (definition.shape()) {
            case FULL -> builder
                    .culling(false)
                    .occluding(false)
                    .cullingIdentical(true);
            case PANE -> builder
                    .culling(false)
                    .occluding(false)
                    .cullingIdentical(false);
        }
    }

    Key tile(Key source, int index) {
        return tileKeys.get(new TileKey(source, index));
    }

    private Map<TileKey, Key> plannedTiles() {
        Map<TileKey, Key> planned = new LinkedHashMap<>();
        Set<Key> outputs = new LinkedHashSet<>();
        for (Key source : ConnectedGlass1114Fusion1312Profile.TEXTURES.keys()) {
            TextureCatalog.Entry entry = ConnectedGlass1114Fusion1312Profile.TEXTURES.get(source);
            int count = entry.layout().columns() * entry.layout().rows();
            for (int index = 0; index < count; index++) {
                Key output = Key.parse("bluemap_connectedglass:tiles/"
                        + source.getNamespace() + "/" + source.getValue() + "/" + index);
                if (!outputs.add(output)) {
                    throw new IllegalArgumentException("synthetic texture key collision");
                }
                planned.put(new TileKey(source, index), output);
            }
        }
        return planned;
    }

    private Map<Key, Texture> cropTiles(Map<TileKey, Key> planned) throws IOException {
        Map<Key, Texture> generated = new LinkedHashMap<>();
        for (Map.Entry<TileKey, Key> request : planned.entrySet()) {
            TileKey tile = request.getKey();
            Texture sourceTexture = resourcePack.getTextures().get(tile.source());
            TextureCatalog.Entry entry = ConnectedGlass1114Fusion1312Profile.TEXTURES.get(tile.source());
            if (sourceTexture == null || entry == null) {
                throw new IOException("required source sheet is missing");
            }
            BufferedImage sheet = sourceTexture.getTextureImage();
            if (!validBakedSheetDimensions(sheet, entry)) {
                throw new IOException("baked source sheet dimensions changed");
            }
            int tileWidth = entry.width() / entry.layout().columns();
            int tileHeight = entry.height() / entry.layout().physicalRows();
            int x = tile.index() % entry.layout().columns() * tileWidth;
            int y = tile.index() / entry.layout().columns() * tileHeight;
            if (tile.index() >= entry.layout().columns() * entry.layout().rows()
                    || x + tileWidth > sheet.getWidth()
                    || y + tileHeight > sheet.getHeight()) {
                throw new IOException("sheet tile leaves active logical crop");
            }
            BufferedImage copy = new BufferedImage(
                    tileWidth, tileHeight, BufferedImage.TYPE_INT_ARGB
            );
            Graphics2D graphics = copy.createGraphics();
            try {
                graphics.drawImage(sheet, -x, -y, null);
            } finally {
                graphics.dispose();
            }
            generated.put(request.getValue(), Texture.from(request.getValue(), copy));
        }
        return generated;
    }

    static boolean validBakedSheetDimensions(
            BufferedImage sheet,
            TextureCatalog.Entry entry
    ) {
        return sheet.getWidth() == entry.width() && sheet.getHeight() == entry.height();
    }

    private record TileKey(Key source, int index) {
    }
}
