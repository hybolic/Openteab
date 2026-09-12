import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { type ExtendedProperties, PageIcons} from "../utils/ExtendedPageData";

type FishingCalibrationItem = {
    key: string;
    label: string;
    isRegion?: boolean;
    fallback: number[];
};

export default function FishingPage({langData}:ExtendedProperties) {
    if (!langData) return
    if (!PageIcons) return
    const { config, saveConfig, error } = useConfig();

    const LABELS = langData.fishing.fishing_calibrations_labels
    const FISHING_CALIBRATIONS: FishingCalibrationItem[] = [
        { key: "fishing_detect_pixel",              label: LABELS.fishing_detect_pixel, fallback: [1176, 836] },
        { key: "fishing_click_position",            label: LABELS.fishing_click_position, fallback: [862, 843] },
        { key: "fishing_midbar_sample_pos",         label: LABELS.fishing_midbar_sample_pos, fallback: [955, 767] },
        { key: "fishing_close_button_pos",          label: LABELS.fishing_close_button_pos, fallback: [1113, 342] },
        { key: "fishing_bar_region",                label: LABELS.fishing_bar_region, isRegion: true, fallback: [757, 762, 405, 21] },
        { key: "fishing_flarg_dialogue_box",        label: LABELS.fishing_flarg_dialogue_box, fallback: [1046, 782] },
        { key: "fishing_shop_open_button",          label: LABELS.fishing_shop_open_button, fallback: [616, 938] },
        { key: "fishing_shop_sell_tab",             label: LABELS.fishing_shop_sell_tab, fallback: [1285, 312] },
        { key: "fishing_shop_close_button",         label: LABELS.fishing_shop_close_button, fallback: [1458, 269] },
        { key: "fishing_shop_first_fish",           label: LABELS.fishing_shop_first_fish, fallback: [827, 404] },
        { key: "fishing_shop_sell_all_button",      label: LABELS.fishing_shop_sell_all_button, fallback: [662, 799] },
        { key: "fishing_confirm_sell_all_button",   label: LABELS.fishing_confirm_sell_all_button, fallback: [800, 619] },
    ];

    function formatPoint(value: any, fallback: number[]) {
        const arr = Array.isArray(value) ? value : fallback;
        return `[${Number(arr[0]) || 0}, ${Number(arr[1]) || 0}]`;
    }

    function formatRegion(value: any, fallback: number[]) {
        const arr = Array.isArray(value) ? value : fallback;
        return `[${Number(arr[0]) || 0}, ${Number(arr[1]) || 0}, ${Number(arr[2]) || 0}, ${Number(arr[3]) || 0}]`;
    }

    if (error) return <div style={{ padding: "20px", color: "red" }}>Error: {error}</div>;
    if (!config) return <div style={{ padding: "20px" }}>Loading...</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    const handleFishingFailsafeToggle = (enabled: boolean) => {
        if (!enabled) {
            updateConfig("fishing_failsafe_rejoin", false);
            return;
        }

        const reconnectEnabled = Boolean(config.auto_reconnect);
        if (!reconnectEnabled) {
            updateConfig("fishing_failsafe_rejoin", false);
            alert("you need to enable reconnect feature for fishing failsafe to work");
            if (typeof (window as any).onNavigateTab === "function") {
                (window as any).onNavigateTab("misc");
            }
            return;
        }

        updateConfig("fishing_failsafe_rejoin", true);
    };

    const handleFishingMerchantMTPToggle = (enabled: boolean) => {
        if (enabled && config.fishing_use_merchant_ocr_every_x_fish) {
            alert("Please disable 'Check merchant on roblox chat (OCR) every x fishes' before enabling the Auto Merchant using Merchant Teleporter every x fishes.");
            return;
        }
        updateConfig("fishing_use_merchant_every_x_fish", enabled);
    };

    const handleFishingMerchantOCRToggle = (enabled: boolean) => {
        if (enabled && config.fishing_use_merchant_every_x_fish) {
            alert("Please disable 'Use merchant teleporter every x fishes' before enabling merchant OCR detection.");
            return;
        }
        updateConfig("fishing_use_merchant_ocr_every_x_fish", enabled);
    };

    const fishingMode = config.fishing_mode || false;
    const fishingFailsafe = config.fishing_failsafe_rejoin || false;
    const fishSellingEnabled = config.fishing_enable_selling || false;
    const equipAuraBeforeMovement = config.fishing_equip_aura_before_movement || false;
    const fishingMerchantEnabled = config.fishing_use_merchant_every_x_fish || false;
    const fishingBrScEnabled = config.fishing_use_br_sc_every_x_fish || false;

    const displayAllCalibrationsOnScreen = async () => {
        try {
            if ((window as any).pywebview?.api?.display_all_fishing_calibrations_on_screen) {
                await (window as any).pywebview.api.display_all_fishing_calibrations_on_screen(3500);
            }
        } catch (e) {
            console.error("Failed to display fishing calibrations on screen:", e);
            alert("Failed to display fishing calibrations on screen: " + e);
        }
    };

    return (
        <>
            <div className="page-header">
                <h2>{langData.nav.fishing}</h2>
                <p>{langData.fishing.description}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Fishing}</div>
                    <div>
                        <h3>{langData.fishing.fishing_mode}</h3>
                        <p>{langData.fishing.fishing_mode_description}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={langData.fishing.enable_fishing_mode}
                    description={langData.fishing.enable_fishing_mode_description}
                    checked={fishingMode}
                    onChange={(val) => updateConfig("fishing_mode", val)}
                />

                <div className="form-row" style={{ marginTop: "8px" }}>
                    <div className="form-group">
                        <label className="form-label">{langData.fishing.fishing_delay}</label>
                        <input
                            className="form-input"
                            value={config.fishing_actions_delay_ms ?? "100"}
                            onChange={(e) => updateConfig("fishing_actions_delay_ms", e.target.value)}
                            style={{ width: "90px" }}
                        />
                    </div>
                </div>

                <div className="form-row" style={{ marginTop: "15px", marginLeft: "10px", paddingBottom: "10px" }}>
                    <div className="form-group">
                        <label className="form-label" style={{ fontWeight: "bold" }}>{langData.fishing.fishing_path_playback}</label>
                        <p style={{ margin: "2px 0 8px 0", fontSize: "0.85em", color: "var(--text-color)", opacity: 0.8 }}>
                            {langData.fishing.fishing_path_description}
                        </p>
                        <input
                            className="form-input"
                            type="number"
                            step="0.01"
                            min="1.0"
                            max="2.0"
                            value={config.fishing_playback_multiplier ?? "1.0"}
                            onChange={(e) => updateConfig("fishing_playback_multiplier", e.target.value)}
                            onBlur={(e) => {
                                let val = parseFloat(e.target.value);
                                if (isNaN(val) || val < 1.0) updateConfig("fishing_playback_multiplier", "1.0");
                            }}
                            style={{ width: "90px" }}
                        />
                    </div>
                </div>
                {Number(config.fishing_playback_multiplier) < 1 && (
                    <div className="info-banner" style={{ marginTop: "5px", color: "var(--warning-color, #ffaa00)" }}>
                        {langData.fishing.warning}
                    </div>
                )}

                <ToggleSwitch
                    label={langData.fishing.fishing_failsafe}
                    description={langData.fishing.fishing_failsafe_description}
                    checked={fishingFailsafe}
                    onChange={handleFishingFailsafeToggle}
                />

                <ToggleSwitch
                    label={langData.fishing.enable_fish_sell}
                    description={langData.fishing.enable_fish_sell_description}
                    checked={fishSellingEnabled}
                    onChange={(val) => updateConfig("fishing_enable_selling", val)}
                />
                {fishSellingEnabled && (
                    <div className="form-row" style={{ marginTop: "8px" }}>
                        <div className="form-group">
                            <label className="form-label">{langData.fishing.enable_fish_sell_after_x}</label>
                            <input
                                className="form-input"
                                value={config.fishing_sell_after_x_fish ?? "30"}
                                onChange={(e) => updateConfig("fishing_sell_after_x_fish", e.target.value)}
                                style={{ width: "90px" }}
                            />
                        </div>
                        <div className="form-group">
                            <label className="form-label">{langData.fishing.enable_fish_sell_amount}</label>
                            <input
                                className="form-input"
                                value={config.fishing_sell_how_many_fish ?? "1"}
                                onChange={(e) => updateConfig("fishing_sell_how_many_fish", e.target.value)}
                                style={{ width: "90px" }}
                            />
                        </div>
                    </div>
                )}

                <ToggleSwitch
                    label={langData.fishing.equip_aura_before_move}
                    description={langData.fishing.equip_aura_before_move_description}
                    checked={equipAuraBeforeMovement}
                    onChange={(val) => updateConfig("fishing_equip_aura_before_movement", val)}
                />
                {equipAuraBeforeMovement && (
                    <div className="form-row" style={{ marginTop: "8px" }}>
                        <div className="form-group">
                            <label className="form-label">{langData.fishing.equip_aura_before_move_name_to_equip}</label>
                            <input
                                className="form-input"
                                value={config.fishing_movement_aura_name || ""}
                                onChange={(e) => updateConfig("fishing_movement_aura_name", e.target.value)}
                                style={{ width: "220px" }}
                                placeholder={langData.fishing.equip_aura_before_move_enter_name}
                            />
                        </div>
                    </div>
                )}

                <ToggleSwitch
                    label={langData.fishing.merchant_tele}
                    description={langData.fishing.merchant_tele_description}
                    checked={fishingMerchantEnabled}
                    onChange={handleFishingMerchantMTPToggle}
                />
                {fishingMerchantEnabled && (
                    <div className="form-row" style={{ marginTop: "8px" }}>
                        <div className="form-group">
                            <label className="form-label">{langData.fishing.merchant_tele_use_every_x}</label>
                            <input
                                className="form-input"
                                value={config.fishing_merchant_every_x_fish ?? "30"}
                                onChange={(e) => updateConfig("fishing_merchant_every_x_fish", e.target.value)}
                                style={{ width: "90px" }}
                            />
                        </div>
                    </div>
                )}

                <ToggleSwitch
                    label={langData.fishing.merchant_ocr}
                    description={langData.fishing.merchant_ocr_description}
                    checked={config.fishing_use_merchant_ocr_every_x_fish || false}
                    onChange={handleFishingMerchantOCRToggle}
                />
                {config.fishing_use_merchant_ocr_every_x_fish && (
                    <div className="form-row" style={{ marginTop: "8px" }}>
                        <div className="form-group">
                            <label className="form-label">{langData.fishing.merchant_ocr_use_every_x}</label>
                            <input
                                className="form-input"
                                value={config.fishing_merchant_ocr_every_x_fish_amt ?? "30"}
                                onChange={(e) => updateConfig("fishing_merchant_ocr_every_x_fish_amt", e.target.value)}
                                style={{ width: "90px" }}
                            />
                        </div>
                    </div>
                )}

                <ToggleSwitch
                    label={langData.fishing.use_br_sc}
                    description={langData.fishing.use_br_sc_description}
                    checked={fishingBrScEnabled}
                    onChange={(val) => updateConfig("fishing_use_br_sc_every_x_fish", val)}
                />
                {fishingBrScEnabled && (
                    <div className="form-row" style={{ marginTop: "8px" }}>
                        <div className="form-group">
                            <label className="form-label">{langData.fishing.use_br_sc_use_every_x}</label>
                            <input
                                className="form-input"
                                value={config.fishing_br_sc_every_x_fish ?? "30"}
                                onChange={(e) => updateConfig("fishing_br_sc_every_x_fish", e.target.value)}
                                style={{ width: "90px" }}
                            />
                        </div>
                    </div>
                )}

                {fishingMode && (
                    <div className="info-banner" style={{ marginTop: "10px" }}>
                        {langData.fishing.fishing_mode_warning}
                    </div>
                )}
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Fishing_cal}</div>
                    <div>
                        <h3>{langData.fishing.fishing_calibration}</h3>
                        <p>{langData.fishing.fishing_calibration_description}</p>
                    </div>
                </div>

                <div style={{ marginBottom: "12px" }}>
                    <button
                        className="btn btn-sm"
                        style={{ whiteSpace: "nowrap", padding: "6px 12px" }}
                        onClick={displayAllCalibrationsOnScreen}
                    >
                        {langData.fishing.osd_calibration}
                    </button>
                </div>

                <div className="settings-grid">
                    {FISHING_CALIBRATIONS.map((item) => (
                        <div
                            key={item.key}
                            className="setting-row"
                            style={{ display: "grid", gridTemplateColumns: "1fr auto", alignItems: "center", gap: "8px" }}
                        >
                            <span className="setting-label">{item.label}</span>
                            <code>
                                {item.isRegion
                                    ? formatRegion((config as any)[item.key], item.fallback)
                                    : formatPoint((config as any)[item.key], item.fallback)}
                            </code>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}