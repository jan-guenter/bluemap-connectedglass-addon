/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.connectedglass.profile;

import java.util.Map;
import java.util.Set;

/** Exact All the Mons 1.2.0 ConnectedGlass/Fusion profile. */
public final class ConnectedGlass1114Fusion1312Profile {

    public static final String PROFILE_ID = "connectedglass-fusion-1.1.14-1.3.12";
    public static final String CONNECTEDGLASS_SHA256 =
            "e5b2a1cd8ef1b8a49a322aeccfc5cd9a53d8303613b9f30718f12a1e525d49fe";
    public static final long CONNECTEDGLASS_SIZE = 819_976L;
    public static final String FUSION_SHA256 =
            "17f5215648a98bcde4134577b013200dbf363273ae282449c51408ae8346f2fa";
    public static final long FUSION_SIZE = 923_270L;
    public static final int ALL_BLOCK_COUNT = 119;
    public static final int ROUTED_BLOCK_COUNT = 119;
    public static final int ROUTED_STATE_COUNT = 1_700;
    public static final int STOCK_BLOCK_COUNT = 0;
    public static final int STOCK_STATE_COUNT = 0;
    public static final int DIRECT_MODEL_COUNT = 425;
    public static final int MODEL_COUNT = 430;
    public static final int TEXTURE_COUNT = 119;
    public static final int METADATA_COUNT = 68;
    public static final int MODIFIER_COUNT = 1;
    public static final int RESOURCE_COUNT = 737;
    public static final int HOST_MODEL_COUNT = 3;
    public static final String DEFINITIONS_SHA256 =
            "7a6fae7eff1af518044ac1ccd31fe18965403b09c7c6a1733ee6d119b196ec2e";
    public static final String RESOURCES_SHA256 =
            "fc8ec7afadcb3fd22566a8879a1cb03e14c880d32803e6ba01d0a751f33030c0";
    public static final String TEXTURES_SHA256 =
            "4f85fd5084dd1a78c1882d3f34cc4535f3268dd2a65bdfb90a39cc5346019363";
    public static final String HOST_MODELS_SHA256 =
            "7eddb8d22e773bea816d180e8fe93d89ab7e0bd770e8520a0eb15b6a573d0230";

    public static final DefinitionCatalog CATALOG = DefinitionCatalog.load(
            "/bluemap-connectedglass/profiles/connectedglass/1.1.14-fusion-1.3.12/definitions.tsv",
            ROUTED_BLOCK_COUNT,
            DEFINITIONS_SHA256
    );
    public static final Map<String, ConnectedGlassDefinition> DEFINITIONS = CATALOG.definitions();
    public static final Set<String> ROUTED_BLOCKS = DEFINITIONS.keySet();
    public static final ResourceManifest RESOURCES = ResourceManifest.load(
            "/bluemap-connectedglass/profiles/connectedglass/1.1.14-fusion-1.3.12/required-resources.tsv",
            RESOURCE_COUNT,
            RESOURCES_SHA256
    );
    public static final TextureCatalog TEXTURES = TextureCatalog.load(
            "/bluemap-connectedglass/profiles/connectedglass/1.1.14-fusion-1.3.12/textures.tsv",
            TEXTURE_COUNT,
            TEXTURES_SHA256
    );
    public static final ResourceManifest HOST_MODELS = ResourceManifest.load(
            "/bluemap-connectedglass/profiles/connectedglass/1.1.14-fusion-1.3.12/host-models.tsv",
            HOST_MODEL_COUNT,
            HOST_MODELS_SHA256,
            "minecraft"
    );

    private ConnectedGlass1114Fusion1312Profile() {
    }
}
