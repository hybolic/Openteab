import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { type ExtendedProperties, PageIcons } from "../utils/ExtendedPageData";

export default function AurasPage({langData}: ExtendedProperties) {
    console.log("LOADING")
    if (!langData) { console.log("Error Loading LangData!"); return <div>Error Loading LangData!</div>}

    console.log(langData)
    const NavLang = langData.nav
    const AuraPageLang = langData.auras
    const AuraDetection = AuraPageLang.detection
    const AuraRecording = AuraPageLang.recording
    const { config, saveConfig, error } = useConfig();

    if (error) return <div style={{ padding: "20px", color: "red" }}>Error: {error}</div>;
    if (!config) return <div style={{ padding: "20px" }}>Loading...</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    return (
        <>
            <div className="page-header">
                <h2>{NavLang.auras}</h2>
                <p>{AuraPageLang.header}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Auras}</div>
                    <div>
                        <h3>{AuraDetection.aura_detection}</h3>
                        <p>{AuraDetection.detect_notify}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={AuraDetection.enable_aura_detection}
                    description={AuraDetection.enable_aura_detection_description}
                    checked={config.enable_aura_detection || false}
                    onChange={(val) => updateConfig("enable_aura_detection", val)}
                />

                {config.enable_aura_detection && (
                    <>
                        <ToggleSwitch
                            label={AuraDetection.aura_screenshot}
                            description={AuraDetection.aura_screenshot_description}
                            checked={config.aura_detection_screenshot || false}
                            onChange={(val) => updateConfig("aura_detection_screenshot", val)}
                        />

                        <div className="form-row" style={{ marginTop: "10px" }}>
                            <div className="form-group">
                                <label className="form-label">{AuraDetection.ping_min_rarity}</label>
                                <input
                                    className="form-input"
                                    value={config.ping_minimum || "100000"}
                                    onChange={(e) => updateConfig("ping_minimum", e.target.value)}
                                    style={{ width: "140px" }}
                                />
                            </div>
                            <div className="form-group">
                                <label className="form-label">{langData.common.discord_user_id}</label>
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
                            <label className="form-label">{AuraDetection.force_ping_auras}</label>
                            <input
                                className="form-input"
                                value={config.force_ping_auras || ""}
                                onChange={(e) => updateConfig("force_ping_auras", e.target.value)}
                                placeholder={AuraPageLang.placeholder}
                                style={{ width: "100%" }}
                            />
                            <small style={{ color: "var(--text-muted)", fontSize: "12px", marginTop: "4px", display: "block" }}>
                                {AuraDetection.ping_help}
                            </small>
                        </div>
                    </>
                )}
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Record}</div>
                    <div>
                        <h3>{AuraRecording.aura_recoding}</h3>
                        <p>{AuraRecording.autoclip_when_rollled}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={AuraRecording.enable_recording}
                    description={AuraRecording.enable_recording_description}
                    checked={config.enable_aura_record || false}
                    onChange={(val) => updateConfig("enable_aura_record", val)}
                />

                {config.enable_aura_record && (
                    <>
                        <div className="form-row" style={{ marginTop: "10px" }}>
                            <div className="form-group">
                                <label className="form-label">{AuraRecording.record_keybind}</label>
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
                                        {AuraRecording.test_keybind}
                                    </button>
                                    <small style={{ color: "var(--text-muted)", fontSize: "11px", whiteSpace: "nowrap" }}>
                                        {AuraRecording.keyboard_delay}
                                    </small>
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="form-label">{AuraRecording.record_min_rarity}</label>
                                <input
                                    className="form-input"
                                    value={config.aura_record_minimum || "100000"}
                                    onChange={(e) => updateConfig("aura_record_minimum", e.target.value)}
                                    style={{ width: "140px" }}
                                />
                            </div>
                        </div>

                        <div className="form-group" style={{ marginTop: "10px" }}>
                            <label className="form-label">{AuraRecording.force_record}</label>
                            <input
                                className="form-input"
                                value={config.force_record_auras || ""}
                                onChange={(e) => updateConfig("force_record_auras", e.target.value)}
                                placeholder={AuraPageLang.placeholder}
                                style={{ width: "100%" }}
                            />
                            <small style={{ color: "var(--text-muted)", fontSize: "12px", marginTop: "4px", display: "block" }}>
                                {AuraRecording.force_record_description}
                            </small>
                        </div>
                    </>
                )}
            </div>
        </>
    );
}