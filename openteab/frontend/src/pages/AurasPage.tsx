import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { PageIcons } from "../utils/ExtendedPageData";
import { Translate } from "../utils/ExtendedPageData";

export default function AurasPage() {
    console.log("LOADING")
    const { config, saveConfig, error } = useConfig();

    if (error) return <div style={{ padding: "20px", color: "red" }}>{Translate("common.error",[{from:"error",to:error}])}</div>;
    if (!config) return <div style={{ padding: "20px" }}>{Translate("common.loading")}</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("nav.auras")}</h2>
                <p>{Translate("auras.header")}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Auras}</div>
                    <div>
                        <h3>{Translate("auras.detection.aura_detection")}</h3>
                        <p>{Translate("auras.detection.detect_notify")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("auras.detection.enable_aura_detection")}
                    description={Translate("auras.detection.enable_aura_detection_description")}
                    checked={config.enable_aura_detection || false}
                    onChange={(val) => updateConfig("enable_aura_detection", val)}
                />

                {config.enable_aura_detection && (
                    <>
                        <ToggleSwitch
                            label={Translate("auras.detection.aura_screenshot")}
                            description={Translate("auras.detection.aura_screenshot_description")}
                            checked={config.aura_detection_screenshot || false}
                            onChange={(val) => updateConfig("aura_detection_screenshot", val)}
                        />

                        <div className="form-row" style={{ marginTop: "10px" }}>
                            <div className="form-group">
                                <label className="form-label">{Translate("auras.detection.ping_min_rarity")}</label>
                                <input
                                    className="form-input"
                                    value={config.ping_minimum || "100000"}
                                    onChange={(e) => updateConfig("ping_minimum", e.target.value)}
                                    style={{ width: "140px" }}
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">{Translate("common.discord_user_id")}</label>
                                <input
                                    className="form-input"
                                    value={config.aura_user_id || ""}
                                    onChange={(e) => updateConfig("aura_user_id", e.target.value)}
                                    placeholder="123456789012345678"
                                    style={{ width: "220px" }}
                                />
                            </div>
                        </div>

                        <div className="form-group" style={{ marginTop: "10px" }}>
                            <label className="form-label">{Translate("auras.detection.force_ping_auras")}</label>
                            <input
                                className="form-input"
                                value={config.force_ping_auras || ""}
                                onChange={(e) => updateConfig("force_ping_auras", e.target.value)}
                                placeholder={Translate("auras.placeholder")}
                                style={{ width: "100%" }}
                            />
                            <small style={{ color: "var(--text-muted)", fontSize: "12px", marginTop: "4px", display: "block" }}>
                                {Translate("auras.detection.ping_help")}
                            </small>
                        </div>
                    </>
                )}
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Record}</div>
                    <div>
                        <h3>{Translate("auras.recording.aura_recoding")}</h3>
                        <p>{Translate("auras.recording.autoclip_when_rollled")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("auras.recording.enable_recording")}
                    description={Translate("auras.recording.enable_recording_description")}
                    checked={config.enable_aura_record || false}
                    onChange={(val) => updateConfig("enable_aura_record", val)}
                />

                {config.enable_aura_record && (
                    <>
                        <div className="form-row" style={{ marginTop: "10px" }}>
                            <div className="form-group">
                                <label className="form-label">{Translate("common.keybind.record")}</label>
                                <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
                                    <input
                                        className="form-input"
                                        value={config.aura_record_keybind || "F8"}
                                        onChange={(e) => updateConfig("aura_record_keybind", e.target.value)}
                                        style={{ width: "100px" }}
                                    />
                                    <button
                                        className="btn btn-accent"
                                        onClick={() => {
                                            if ((window as any).pywebview) {
                                                (window as any).pywebview.api.test_aura_keybind();
                                            }
                                        }}
                                        style={{ padding: "8px 16px", whiteSpace: "nowrap" }}
                                    >
                                        {Translate("common.keybind.test")}
                                    </button>
                                    <small style={{ color: "var(--text-muted)", fontSize: "11px", whiteSpace: "nowrap" }}>
                                        {Translate("common.keybind.fire_after_x")}
                                    </small>
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="form-label">{Translate("auras.recording.record_min_rarity")}</label>
                                <input
                                    className="form-input"
                                    value={config.aura_record_minimum || "100000"}
                                    onChange={(e) => updateConfig("aura_record_minimum", e.target.value)}
                                    style={{ width: "140px" }}
                                />
                            </div>
                        </div>

                        <div className="form-group" style={{ marginTop: "10px" }}>
                            <label className="form-label">{Translate("auras.recording.force_record")}</label>
                            <input
                                className="form-input"
                                value={config.force_record_auras || ""}
                                onChange={(e) => updateConfig("force_record_auras", e.target.value)}
                                placeholder={Translate("auras.placeholder")}
                                style={{ width: "100%" }}
                            />
                            <small style={{ color: "var(--text-muted)", fontSize: "12px", marginTop: "4px", display: "block" }}>
                                {Translate("auras.recording.force_record_description")}
                            </small>
                        </div>
                    </>
                )}
            </div>
        </>
    );
}