/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.profile;

import java.util.Locale;

/** Stable geometry families in the exact routed ConnectedGlass roster. */
public enum ShapeFamily {
    FULL("full", 1),
    PANE("pane", 32);

    private final String wireName;
    private final int legalStates;

    ShapeFamily(String wireName, int legalStates) {
        this.wireName = wireName;
        this.legalStates = legalStates;
    }

    public String wireName() {
        return wireName;
    }

    public int legalStates() {
        return legalStates;
    }

    public static ShapeFamily parse(String value) {
        for (ShapeFamily family : values()) {
            if (family.wireName.equals(value.toLowerCase(Locale.ROOT))) {
                return family;
            }
        }
        throw new IllegalArgumentException("unknown ConnectedGlass shape family");
    }
}
