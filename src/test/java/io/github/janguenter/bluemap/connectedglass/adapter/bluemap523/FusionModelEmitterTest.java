/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap523;

import de.bluecolored.bluemap.core.util.Direction;
import de.bluecolored.bluemap.core.util.Key;
import de.bluecolored.bluemap.core.world.BlockState;
import io.github.janguenter.bluemap.connectedglass.profile.ShapeFamily;
import io.github.janguenter.bluemap.connectedglass.profile.TextureLayout;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FusionModelEmitterTest {

    @Test
    void piecedClippingDropsZeroAreaSlabSeams() {
        assertEquals(4, FusionModelEmitter.piecedPartCount(0F, 0F, 1F, 1F));
        assertEquals(2, FusionModelEmitter.piecedPartCount(0F, 0.5F, 1F, 1F));
        assertEquals(1, FusionModelEmitter.piecedPartCount(0F, 0.5F, 0.5F, 1F));
        assertEquals(0, FusionModelEmitter.piecedPartCount(0F, 0.5F, 1F, 0.5F));
    }

    @Test
    void plainEdgeTexturesDoNotNeedConnectionFrames() {
        assertFalse(FusionModelEmitter.requiresConnectionFrame(TextureLayout.PLAIN));
        assertTrue(FusionModelEmitter.requiresConnectionFrame(TextureLayout.PIECED));
    }

    @Test
    void fullCubesCullSameIdButNeverOtherIds() {
        BlockState clear = state("connectedglass:clear_glass", Map.of());
        assertTrue(FusionModelEmitter.sameRoutedFaceCulls(
                ShapeFamily.FULL, Direction.NORTH, clear, clear
        ));
        assertFalse(FusionModelEmitter.sameRoutedFaceCulls(
                ShapeFamily.FULL,
                Direction.NORTH,
                clear,
                state("connectedglass:clear_glass_red", Map.of())
        ));
        BlockState vanilla = state("minecraft:glass", Map.of());
        assertFalse(FusionModelEmitter.sameRoutedFaceCulls(
                ShapeFamily.FULL, Direction.NORTH, vanilla, vanilla
        ));
    }

    @Test
    void panesCullOnlyReciprocalHorizontalArmsAndIgnoreWaterlogging() {
        BlockState own = pane("true", "false", "false", "false", "false");
        BlockState reciprocalWet = pane("false", "false", "true", "false", "true");
        BlockState nonreciprocal = pane("false", "false", "false", "false", "false");
        assertTrue(FusionModelEmitter.sameRoutedFaceCulls(
                ShapeFamily.PANE, Direction.NORTH, own, reciprocalWet
        ));
        assertFalse(FusionModelEmitter.sameRoutedFaceCulls(
                ShapeFamily.PANE, Direction.NORTH, own, nonreciprocal
        ));
        assertFalse(FusionModelEmitter.sameRoutedFaceCulls(
                ShapeFamily.PANE, Direction.UP, own, reciprocalWet
        ));
    }

    @Test
    void verticalPaneCapsCullOnlyTheirOverlappingGeometricPiece() {
        BlockState own = pane("true", "false", "false", "false", "false");
        BlockState neighbor = pane("true", "false", "false", "false", "true");
        assertTrue(FusionModelEmitter.shouldCullPaneCap(
                ShapeFamily.PANE, Direction.UP, own, neighbor, 0.5F, 0.5F
        ));
        assertTrue(FusionModelEmitter.shouldCullPaneCap(
                ShapeFamily.PANE, Direction.UP, own, neighbor, 0.5F, 0.2F
        ));
        assertFalse(FusionModelEmitter.shouldCullPaneCap(
                ShapeFamily.PANE, Direction.UP, own, neighbor, 0.8F, 0.5F
        ));
        assertFalse(FusionModelEmitter.shouldCullPaneCap(
                ShapeFamily.PANE,
                Direction.UP,
                own,
                state("connectedglass:clear_glass_red_pane", neighbor.getProperties()),
                0.5F,
                0.5F
        ));
        assertFalse(FusionModelEmitter.shouldCullPaneCap(
                ShapeFamily.PANE, Direction.NORTH, own, neighbor, 0.5F, 0.5F
        ));
    }

    private static BlockState pane(
            String north,
            String east,
            String south,
            String west,
            String waterlogged
    ) {
        return state("connectedglass:clear_glass_pane", Map.of(
                "north", north,
                "east", east,
                "south", south,
                "west", west,
                "waterlogged", waterlogged
        ));
    }

    private static BlockState state(String id, Map<String, String> properties) {
        return new BlockState(Key.parse(id), properties);
    }
}
