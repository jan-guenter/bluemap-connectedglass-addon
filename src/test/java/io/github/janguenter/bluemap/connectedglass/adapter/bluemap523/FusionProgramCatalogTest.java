/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap523;

import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.connectedglass.profile.ConnectedGlass1114Fusion1312Profile;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FusionProgramCatalogTest {

    @Test
    void parsesEveryExactCustomModelAndResolvesItsDefaultPredicate()
            throws IOException {
        Map<String, byte[]> models = exactModels(required("connectedglassJar"));
        FusionProgramCatalog catalog = FusionProgramCatalog.parse(models);
        assertEquals(425, catalog.size());

        long sameBlock = catalog.programs().values().stream()
                .filter(program -> program.predicate("unused") instanceof FusionPredicate.SameBlock)
                .count();
        long compound = catalog.programs().values().stream()
                .filter(program -> program.predicate("unused") instanceof FusionPredicate.Any)
                .count();
        assertEquals(68, sameBlock);
        assertEquals(357, compound);

        for (FusionProgramCatalog.Program program : catalog.programs().values()) {
            assertFalse(program.textures().isEmpty());
            assertEquals(Set.of("default"), program.connections().keySet());
            assertFalse(program.predicate("pane") instanceof FusionPredicate.Never,
                    () -> "unresolved default predicate in " + program.model());
            assertEquals(program.predicate("pane"), program.predicate("edge"));
        }
    }

    @Test
    void everyVariantAndMultipartApplyHasAnExactProgram() throws IOException {
        Path jar = required("connectedglassJar");
        FusionProgramCatalog catalog = FusionProgramCatalog.parse(exactModels(jar));
        int selected = 0;
        Set<Key> unique = new HashSet<>();
        try (ZipFile zip = new ZipFile(jar.toFile())) {
            for (String path : ConnectedGlass1114Fusion1312Profile.RESOURCES.entries().keySet()) {
                if (!path.contains("/blockstates/")) {
                    continue;
                }
                String json = new String(
                        zip.getInputStream(zip.getEntry(path)).readAllBytes(),
                        StandardCharsets.UTF_8
                );
                com.google.gson.JsonObject root = com.google.gson.JsonParser.parseString(json)
                        .getAsJsonObject();
                List<Key> selections = new java.util.ArrayList<>();
                if (root.has("variants")) {
                    for (Map.Entry<String, com.google.gson.JsonElement> variant
                            : root.getAsJsonObject("variants").entrySet()) {
                        addModels(variant.getValue(), selections);
                    }
                }
                if (root.has("multipart")) {
                    for (com.google.gson.JsonElement part : root.getAsJsonArray("multipart")) {
                        addModels(part.getAsJsonObject().get("apply"), selections);
                    }
                }
                for (Key model : selections) {
                    assertNotNull(catalog.get(model), () -> "missing program for " + model);
                    unique.add(model);
                    selected++;
                }
            }
        }
        assertEquals(527, selected);
        assertEquals(425, unique.size());
    }

    private static void addModels(
            com.google.gson.JsonElement selection,
            List<Key> models
    ) {
        if (selection.isJsonArray()) {
            selection.getAsJsonArray().forEach(value -> addModels(value, models));
            return;
        }
        com.google.gson.JsonObject object = selection.getAsJsonObject();
        models.add(Key.parse(object.get("model").getAsString()));
    }

    private static Map<String, byte[]> exactModels(Path jar) throws IOException {
        Map<String, byte[]> models = new HashMap<>();
        try (ZipFile zip = new ZipFile(jar.toFile())) {
            ConnectedGlass1114Fusion1312Profile.RESOURCES.entries().forEach((path, manifest) -> {
                if (!manifest.kind().equals("model")) {
                    return;
                }
                ZipEntry entry = zip.getEntry(path);
                assertNotNull(entry, path);
                try {
                    models.put(path, zip.getInputStream(entry).readAllBytes());
                } catch (IOException exception) {
                    throw new java.io.UncheckedIOException(exception);
                }
            });
        } catch (java.io.UncheckedIOException exception) {
            throw exception.getCause();
        }
        assertEquals(430, models.size());
        assertTrue(models.keySet().stream().allMatch(
                path -> path.startsWith("assets/connectedglass/models/")
        ));
        return models;
    }

    private static Path required(String property) {
        String value = System.getProperty(property);
        if (value == null || value.isBlank()) {
            throw new AssertionError("missing exact test artifact property: " + property);
        }
        return Path.of(value);
    }
}
