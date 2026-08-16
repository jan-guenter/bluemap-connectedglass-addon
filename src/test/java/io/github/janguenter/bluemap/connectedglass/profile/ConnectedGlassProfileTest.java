/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.profile;

import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.Map;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ConnectedGlassProfileTest {

    @Test
    void locksRouteAndLegalStateCensus() {
        Map<ShapeFamily, Long> shapes = ConnectedGlass1114Fusion1312Profile.DEFINITIONS.values()
                .stream()
                .collect(Collectors.groupingBy(
                        ConnectedGlassDefinition::shape,
                        () -> new EnumMap<>(ShapeFamily.class),
                        Collectors.counting()
        ));
        assertEquals(Map.of(
                ShapeFamily.FULL, 68L,
                ShapeFamily.PANE, 51L
        ), shapes);
        int legalStates = ConnectedGlass1114Fusion1312Profile.DEFINITIONS.values()
                .stream().mapToInt(ConnectedGlassDefinition::legalStates).sum();
        assertEquals(1_700, legalStates);
        assertEquals(119, ConnectedGlass1114Fusion1312Profile.ROUTED_BLOCKS.size());
        assertTrue(ConnectedGlass1114Fusion1312Profile.ROUTED_BLOCKS.stream()
                .allMatch(id -> id.startsWith("connectedglass:")));
        assertFalse(ConnectedGlass1114Fusion1312Profile.ROUTED_BLOCKS.stream()
                .anyMatch(id -> id.startsWith("fusion:")));
    }

    @Test
    void locksInstalledResourceClosureAndLayoutCensus() {
        Map<String, Long> resources = ConnectedGlass1114Fusion1312Profile.RESOURCES.entries()
                .values().stream()
                .collect(Collectors.groupingBy(
                        ResourceManifest.Entry::kind, Collectors.counting()
        ));
        assertEquals(Map.of(
                "blockstate", 119L,
                "model", 430L,
                "texture", 119L,
                "metadata", 68L,
                "modifier", 1L
        ), resources);
        Map<TextureLayout, Long> layouts = ConnectedGlass1114Fusion1312Profile.TEXTURES.entries()
                .values().stream()
                .collect(Collectors.groupingBy(
                        TextureCatalog.Entry::layout, Collectors.counting()
        ));
        assertEquals(Map.of(
                TextureLayout.PLAIN, 51L,
                TextureLayout.PIECED, 68L
        ), layouts);
        assertEquals(3, ConnectedGlass1114Fusion1312Profile.HOST_MODELS.entries().size());
        assertTrue(ConnectedGlass1114Fusion1312Profile.HOST_MODELS.entries().keySet().stream()
                .allMatch(path -> path.startsWith("assets/minecraft/models/block/")));
        assertTrue(ConnectedGlass1114Fusion1312Profile.HOST_MODELS.entries().containsKey(
                "assets/minecraft/models/block/block.json"
        ));
        assertTrue(ConnectedGlass1114Fusion1312Profile.HOST_MODELS.entries().containsKey(
                "assets/minecraft/models/block/cube_all.json"
        ));
        assertTrue(ConnectedGlass1114Fusion1312Profile.RESOURCES.entries().containsKey(
                "assets/connectedglass/fusion/model_modifiers/blocks/pane_culling_fix.json"
        ));
        ConnectedGlass1114Fusion1312Profile.TEXTURES.entries().forEach((key, entry) -> {
            assertTrue(key.getFormatted().startsWith("connectedglass:"));
            assertEquals(16, entry.width() / entry.layout().columns());
            assertEquals(16, entry.height() / entry.layout().physicalRows());
        });
    }
}
