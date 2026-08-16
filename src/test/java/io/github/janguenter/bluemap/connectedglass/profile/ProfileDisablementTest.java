/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.profile;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ProfileDisablementTest {

    @Test
    void mergesNormalizedPropertyAndEnvironmentLists() {
        ProfileDisablement disabled = ProfileDisablement.from(
                "connectedglass-fusion-1.1.14-1.3.12, invalid value",
                "CONNECTEDGLASS-FUSION-1.1.14-1.3.12,other"
        );
        assertTrue(disabled.isDisabled(ConnectedGlass1114Fusion1312Profile.PROFILE_ID));
        assertEquals(2, disabled.disabledProfiles().size());
    }
}
