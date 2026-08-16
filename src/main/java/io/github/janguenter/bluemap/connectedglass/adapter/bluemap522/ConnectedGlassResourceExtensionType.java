/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.adapter.bluemap522;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.connectedglass.activation.ConnectedGlassRuntime;

/** Resource-pack extension factory registered before resource loading begins. */
final class ConnectedGlassResourceExtensionType
        implements ResourcePack.Extension<ConnectedGlassResourceExtension> {

    static final Key KEY = Key.parse("bluemap_connectedglass:exact_profile");

    private final ConnectedGlassRuntime runtime;

    ConnectedGlassResourceExtensionType(ConnectedGlassRuntime runtime) {
        this.runtime = runtime;
    }

    @Override
    public Key getKey() {
        return KEY;
    }

    @Override
    public ConnectedGlassResourceExtension create(ResourcePack pack) {
        return new ConnectedGlassResourceExtension(pack, runtime);
    }
}
