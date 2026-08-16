/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap522;

import de.bluecolored.bluemap.core.util.Key;
import de.bluecolored.bluemap.core.util.Tristate;
import de.bluecolored.bluemap.core.world.BlockProperties;
import de.bluecolored.bluemap.core.world.BlockState;
import io.github.janguenter.bluemap.connectedglass.profile.ConnectedGlassDefinition;
import io.github.janguenter.bluemap.connectedglass.profile.ShapeFamily;
import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ConnectedGlassStateSchemaTest {

    private static final String PANE_ID = "connectedglass:clear_glass_pane";
    private static final ConnectedGlassDefinition PANE = definition(
            PANE_ID, ShapeFamily.PANE, 32
    );
    private static final ConnectedGlassDefinition FULL = definition(
            "connectedglass:clear_glass", ShapeFamily.FULL, 1
    );

    @Test
    void acceptsEveryExactPaneCombination() {
        for (int mask = 0; mask < 32; mask++) {
            assertTrue(ConnectedGlassStateSchema.accepts(
                    pane(mask), PANE
            ));
        }
    }

    @Test
    void rejectsMissingExtraInvalidAndWrongIdPaneProperties() {
        Map<String, String> valid = new HashMap<>(pane(0).getProperties());
        valid.remove("north");
        assertFalse(ConnectedGlassStateSchema.accepts(state(PANE_ID, valid), PANE));

        valid = new HashMap<>(pane(0).getProperties());
        valid.put("legacy", "false");
        assertFalse(ConnectedGlassStateSchema.accepts(state(PANE_ID, valid), PANE));

        valid = new HashMap<>(pane(0).getProperties());
        valid.put("east", "maybe");
        assertFalse(ConnectedGlassStateSchema.accepts(state(PANE_ID, valid), PANE));

        assertFalse(ConnectedGlassStateSchema.accepts(
                state("connectedglass:clear_glass_red_pane", pane(0).getProperties()),
                PANE
        ));
    }

    @Test
    void fullCubesAcceptOnlyTheirPropertylessNativeState() {
        assertTrue(ConnectedGlassStateSchema.accepts(
                state("connectedglass:clear_glass", Map.of()), FULL
        ));
        assertFalse(ConnectedGlassStateSchema.accepts(
                state("connectedglass:clear_glass", Map.of("legacy", "true")), FULL
        ));
        assertFalse(ConnectedGlassStateSchema.accepts(
                state("connectedglass:clear_glass_red", Map.of()), FULL
        ));
    }

    @Test
    void rejectedPaneAndFullStatesReceiveExplicitSafeProperties() {
        assertSafeProperties(state(PANE_ID, Map.of()), PANE);
        assertSafeProperties(
                state("connectedglass:clear_glass", Map.of("legacy", "true")),
                FULL
        );
    }

    private static void assertSafeProperties(
            BlockState state,
            ConnectedGlassDefinition definition
    ) {
        BlockProperties.Builder builder = BlockProperties.builder();
        ConnectedGlassResourceExtension.applyProperties(state, definition, builder);

        assertEquals(Tristate.FALSE, builder.isCulling());
        assertEquals(Tristate.FALSE, builder.isOccluding());
        assertEquals(Tristate.FALSE, builder.isCullingIdentical());
    }

    private static BlockState pane(int mask) {
        return state(PANE_ID, Map.of(
                "north", bit(mask, 0),
                "east", bit(mask, 1),
                "south", bit(mask, 2),
                "west", bit(mask, 3),
                "waterlogged", bit(mask, 4)
        ));
    }

    private static String bit(int mask, int bit) {
        return (mask & 1 << bit) == 0 ? "false" : "true";
    }

    private static BlockState state(String id, Map<String, String> properties) {
        return new BlockState(Key.parse(id), properties);
    }

    private static ConnectedGlassDefinition definition(
            String id,
            ShapeFamily shape,
            int states
    ) {
        return new ConnectedGlassDefinition(
                id, shape, states, "0".repeat(64), "1".repeat(64)
        );
    }
}
