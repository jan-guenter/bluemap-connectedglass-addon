/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.profile;

import java.util.Objects;

/** Hash-locked blockstate and selected-model metadata for one exact routed block. */
public record ConnectedGlassDefinition(
        String blockId,
        ShapeFamily shape,
        int legalStates,
        String blockstateSha256,
        String directModelsSha256
) {

    public ConnectedGlassDefinition {
        Objects.requireNonNull(blockId, "blockId");
        Objects.requireNonNull(shape, "shape");
        Objects.requireNonNull(blockstateSha256, "blockstateSha256");
        Objects.requireNonNull(directModelsSha256, "directModelsSha256");
        if (!blockId.startsWith("connectedglass:")
                || legalStates != shape.legalStates()
                || !blockstateSha256.matches("[0-9a-f]{64}")
                || !directModelsSha256.matches("[0-9a-f]{64}")) {
            throw new IllegalArgumentException("malformed ConnectedGlass rendering definition");
        }
    }
}
