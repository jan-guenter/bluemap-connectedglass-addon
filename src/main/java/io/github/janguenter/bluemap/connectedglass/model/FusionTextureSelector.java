/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.model;

import io.github.janguenter.bluemap.connectedglass.profile.TextureLayout;

/** Independently authored selector for the exact Connected Glass sheet layouts. */
public final class FusionTextureSelector {

    private static final int[] PIECED_CORNERS = {0, 3, 2, 4, 0, 3, 2, 1};

    private FusionTextureSelector() {
    }

    public static int tile(TextureLayout layout, int mask) {
        if ((mask & ~0xff) != 0) {
            throw new IllegalArgumentException("connection mask must be one byte");
        }
        return switch (layout) {
            case PLAIN -> 0;
            case PIECED -> piecedShortcut(mask);
        };
    }

    public static int piecedCorner(int mask, FusionDirection corner) {
        int index = switch (corner) {
            case TOP_LEFT -> bit(mask, FusionDirection.LEFT)
                    | bit(mask, FusionDirection.TOP) << 1
                    | bit(mask, FusionDirection.TOP_LEFT) << 2;
            case TOP_RIGHT -> bit(mask, FusionDirection.RIGHT)
                    | bit(mask, FusionDirection.TOP) << 1
                    | bit(mask, FusionDirection.TOP_RIGHT) << 2;
            case BOTTOM_LEFT -> bit(mask, FusionDirection.LEFT)
                    | bit(mask, FusionDirection.BOTTOM) << 1
                    | bit(mask, FusionDirection.BOTTOM_LEFT) << 2;
            case BOTTOM_RIGHT -> bit(mask, FusionDirection.RIGHT)
                    | bit(mask, FusionDirection.BOTTOM) << 1
                    | bit(mask, FusionDirection.BOTTOM_RIGHT) << 2;
            default -> throw new IllegalArgumentException("not a pieced corner");
        };
        return PIECED_CORNERS[index];
    }

    private static int piecedShortcut(int mask) {
        int cardinals = cardinalCount(mask);
        if (cardinals == 0) {
            return 0;
        }
        if (mask == 0xff) {
            return 1;
        }
        if (cardinals == 2 && set(mask, FusionDirection.TOP)
                && set(mask, FusionDirection.BOTTOM)) {
            return 2;
        }
        if (cardinals == 2 && set(mask, FusionDirection.LEFT)
                && set(mask, FusionDirection.RIGHT)) {
            return 3;
        }
        if (cardinals == 4 && diagonalCount(mask) == 0) {
            return 4;
        }
        return -1;
    }

    private static int cardinalCount(int mask) {
        return bit(mask, FusionDirection.TOP) + bit(mask, FusionDirection.RIGHT)
                + bit(mask, FusionDirection.BOTTOM) + bit(mask, FusionDirection.LEFT);
    }

    private static int diagonalCount(int mask) {
        return bit(mask, FusionDirection.TOP_RIGHT)
                + bit(mask, FusionDirection.BOTTOM_RIGHT)
                + bit(mask, FusionDirection.BOTTOM_LEFT)
                + bit(mask, FusionDirection.TOP_LEFT);
    }

    private static int bit(int mask, FusionDirection direction) {
        return set(mask, direction) ? 1 : 0;
    }

    private static boolean set(int mask, FusionDirection direction) {
        return (mask & 1 << direction.bit()) != 0;
    }
}
