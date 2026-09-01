/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap523;

import io.github.janguenter.bluemap.connectedglass.profile.TextureCatalog;
import io.github.janguenter.bluemap.connectedglass.profile.TextureLayout;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.URI;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ActiveResourceSchemaValidatorTest {

    private static final TextureCatalog.Entry EXPECTED = new TextureCatalog.Entry(
            TextureLayout.PIECED, 80, 16, "0".repeat(64)
    );

    @Test
    void acceptsPixelOverridesButRejectsLayoutDimensionChanges(@TempDir Path temporary)
            throws IOException {
        Path changedPixels = temporary.resolve("changed.png");
        write(changedPixels, 80, 16, 0xff12ab34);
        assertTrue(ActiveResourceSchemaValidator.validTexture(changedPixels, EXPECTED));

        Path wrongDimensions = temporary.resolve("wrong.png");
        write(wrongDimensions, 79, 16, 0xff12ab34);
        assertFalse(ActiveResourceSchemaValidator.validTexture(wrongDimensions, EXPECTED));
    }

    @Test
    void validatesImagesThroughAnOpenZipFileSystem(@TempDir Path temporary)
            throws IOException {
        Path zip = temporary.resolve("resources.zip");
        URI uri = URI.create("jar:" + zip.toUri());
        try (FileSystem fileSystem = FileSystems.newFileSystem(uri, Map.of("create", "true"))) {
            Path image = fileSystem.getPath("/assets/connectedglass/textures/block/example.png");
            Files.createDirectories(image.getParent());
            write(image, 80, 16, 0xffabcdef);
            assertTrue(ActiveResourceSchemaValidator.validTexture(image, EXPECTED));
        }
    }

    @Test
    void acceptsPlainSixteenPixelEdgesAndRejectsLargerOverrides(@TempDir Path temporary)
            throws IOException {
        TextureCatalog.Entry edge = new TextureCatalog.Entry(
                TextureLayout.PLAIN, 16, 16, "0".repeat(64)
        );
        Path accepted = temporary.resolve("edge.png");
        write(accepted, 16, 16, 0x80445566);
        assertTrue(ActiveResourceSchemaValidator.validTexture(accepted, edge));
        Path rejected = temporary.resolve("large-edge.png");
        write(rejected, 32, 16, 0x80445566);
        assertFalse(ActiveResourceSchemaValidator.validTexture(rejected, edge));
    }

    @Test
    void bakedAtlasRemapsMustPreserveExactSheetDimensions() {
        TextureCatalog.Entry entry = new TextureCatalog.Entry(
                TextureLayout.PIECED, 80, 16, "0".repeat(64)
        );
        assertTrue(ConnectedGlassResourceExtension.validBakedSheetDimensions(
                new BufferedImage(80, 16, BufferedImage.TYPE_INT_ARGB), entry
        ));
        assertFalse(ConnectedGlassResourceExtension.validBakedSheetDimensions(
                new BufferedImage(160, 16, BufferedImage.TYPE_INT_ARGB), entry
        ));
    }

    @Test
    void pngDimensionsAreRejectedBeforeImageDecoding() {
        byte[] header = {
            (byte) 0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
            0, 0, 0, 13, 'I', 'H', 'D', 'R',
            0, 0, 0, 80, 0, 0, 0, 16
        };
        assertTrue(ActiveResourceSchemaValidator.hasExpectedPngHeader(header, 80, 16));
        assertFalse(ActiveResourceSchemaValidator.hasExpectedPngHeader(header, 16, 16));
        assertFalse(ActiveResourceSchemaValidator.hasExpectedPngHeader(
                Arrays.copyOf(header, 23), 80, 16
        ));
        header[0] = 0;
        assertFalse(ActiveResourceSchemaValidator.hasExpectedPngHeader(header, 80, 16));
    }

    private static void write(Path path, int width, int height, int color) throws IOException {
        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
        image.setRGB(width / 2, height / 2, color);
        try (java.io.OutputStream output = Files.newOutputStream(path)) {
            ImageIO.write(image, "png", output);
        }
    }
}
