/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.activation;

import io.github.janguenter.bluemap.connectedglass.adapter.bluemap523.FusionProgramCatalog;

/** Process-scoped state for the single exact Connected Glass/Fusion route. */
public final class ConnectedGlassRuntime {

    public static final String ROUTE_ID = "connectedglass-fusion-1.1.14-1.3.12";
    public static final ConnectedGlassRuntime INSTANCE = new ConnectedGlassRuntime();

    private final RouteActivation route = new RouteActivation(ROUTE_ID);
    private volatile FusionProgramCatalog catalog;

    private ConnectedGlassRuntime() {
    }

    public RouteActivation route() {
        return route;
    }

    public FusionProgramCatalog catalog() {
        return catalog;
    }

    public synchronized void activate(FusionProgramCatalog installedCatalog) {
        catalog = java.util.Objects.requireNonNull(installedCatalog, "installedCatalog");
        route.activate();
    }

    public synchronized void inactive(String detail) {
        catalog = null;
        route.inactive(detail);
    }

    public void disable(String detail) {
        catalog = null;
        route.fail(detail);
    }
}
