/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap522;

import de.bluecolored.bluemap.core.world.BlockState;
import io.github.janguenter.bluemap.connectedglass.profile.ConnectedGlassDefinition;
import io.github.janguenter.bluemap.connectedglass.profile.ShapeFamily;

import java.util.Map;
import java.util.Set;

/** Exact persisted-state boundary for the 119 routed native blocks. */
final class ConnectedGlassStateSchema {

    private static final Set<String> PANE_PROPERTIES = Set.of(
            "north", "east", "south", "west", "waterlogged"
    );
    private static final Set<String> BOOLEAN_VALUES = Set.of("false", "true");

    private ConnectedGlassStateSchema() {
    }

    static boolean accepts(BlockState state, ConnectedGlassDefinition definition) {
        if (state == null || definition == null
                || !definition.blockId().equals(state.getId().getFormatted())) {
            return false;
        }
        Map<String, String> properties = state.getProperties();
        if (definition.shape() == ShapeFamily.FULL) {
            return properties.isEmpty();
        }
        if (definition.shape() != ShapeFamily.PANE
                || !properties.keySet().equals(PANE_PROPERTIES)) {
            return false;
        }
        return properties.values().stream().allMatch(BOOLEAN_VALUES::contains);
    }
}
