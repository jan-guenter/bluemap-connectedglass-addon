/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap522;

import de.bluecolored.bluemap.core.util.Key;
import de.bluecolored.bluemap.core.world.BlockState;
import io.github.janguenter.bluemap.resource.fusion.model.FusionDirection;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FusionPredicateTest {

    private static final BlockState OWN = state(
            "connectedglass:clear_glass_pane",
            Map.of("north", "true", "waterlogged", "false")
    );

    @Test
    void matchStateProjectsOnlyTheListedNativeProperties() {
        BlockState neighbor = state(
                "connectedglass:clear_glass_pane",
                Map.of("north", "true", "waterlogged", "true")
        );
        assertTrue(new FusionPredicate.MatchState(
                "connectedglass:clear_glass_pane", Map.of("north", Set.of("true"))
        ).test(OWN, neighbor, FusionDirection.TOP));
        assertFalse(new FusionPredicate.MatchState(
                "connectedglass:clear_glass_pane", Map.of("north", Set.of("false"))
        ).test(OWN, neighbor, FusionDirection.TOP));
        assertFalse(new FusionPredicate.MatchState(
                "connectedglass:borderless_glass_pane", Map.of("north", Set.of("true"))
        ).test(OWN, neighbor, FusionDirection.TOP));
    }

    @Test
    void sameBlockConnectsWetAndDryStatesButRejectsOtherIdsAndAir() {
        FusionPredicate predicate = new FusionPredicate.SameBlock();
        assertTrue(predicate.test(OWN, state(
                "connectedglass:clear_glass_pane",
                Map.of("north", "false", "waterlogged", "true")
        ), FusionDirection.RIGHT));
        assertFalse(predicate.test(OWN, state(
                "connectedglass:clear_glass_red_pane",
                Map.of("north", "true", "waterlogged", "false")
        ), FusionDirection.RIGHT));
        assertFalse(predicate.test(OWN, BlockState.AIR, FusionDirection.RIGHT));
    }

    @Test
    void directionAndOrNodesUseOrdinaryListedOrderSemantics() {
        FusionPredicate direction = new FusionPredicate.DirectionIn(
                Set.of(FusionDirection.TOP, FusionDirection.TOP_LEFT)
        );
        FusionPredicate block = new FusionPredicate.SameBlock();
        assertTrue(new FusionPredicate.Any(List.of(new FusionPredicate.Never(), block))
                .test(OWN, OWN, FusionDirection.BOTTOM));
        assertTrue(new FusionPredicate.Any(List.of(direction, new FusionPredicate.Never()))
                .test(OWN, BlockState.AIR, FusionDirection.TOP));
        assertFalse(new FusionPredicate.Any(List.of(direction, new FusionPredicate.Never()))
                .test(OWN, BlockState.AIR, FusionDirection.BOTTOM));
    }

    private static BlockState state(String id, Map<String, String> properties) {
        return new BlockState(Key.parse(id), properties);
    }
}
