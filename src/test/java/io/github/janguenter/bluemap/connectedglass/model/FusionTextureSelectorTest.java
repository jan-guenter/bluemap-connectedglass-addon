/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.model;

import io.github.janguenter.bluemap.connectedglass.profile.TextureLayout;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class FusionTextureSelectorTest {

    @Test
    void plainTexturesAlwaysSelectTheirOnlyCell() {
        for (int mask = 0; mask < 256; mask++) {
            assertEquals(0, FusionTextureSelector.tile(TextureLayout.PLAIN, mask));
        }
        assertThrows(IllegalArgumentException.class,
                () -> FusionTextureSelector.tile(TextureLayout.PLAIN, -1));
        assertThrows(IllegalArgumentException.class,
                () -> FusionTextureSelector.tile(TextureLayout.PLAIN, 256));
    }

    @Test
    void locksPiecedShortcutsAndCornerQuadrants() {
        assertEquals(0, FusionTextureSelector.tile(TextureLayout.PIECED, 0x00));
        assertEquals(1, FusionTextureSelector.tile(TextureLayout.PIECED, 0xff));
        assertEquals(2, FusionTextureSelector.tile(TextureLayout.PIECED, 0x11));
        assertEquals(3, FusionTextureSelector.tile(TextureLayout.PIECED, 0x44));
        assertEquals(4, FusionTextureSelector.tile(TextureLayout.PIECED, 0x55));
        assertEquals(-1, FusionTextureSelector.tile(TextureLayout.PIECED, 0x57));
        int[] expected = {0, 3, 2, 4, 0, 3, 2, 1};
        int[] actual = new int[8];
        for (int index = 0; index < 8; index++) {
            int mask = (index & 1) << FusionDirection.LEFT.bit()
                    | ((index >> 1) & 1) << FusionDirection.TOP.bit()
                    | ((index >> 2) & 1) << FusionDirection.TOP_LEFT.bit();
            actual[index] = FusionTextureSelector.piecedCorner(
                    mask, FusionDirection.TOP_LEFT
            );
        }
        assertArrayEquals(expected, actual);
    }
}
