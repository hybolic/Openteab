import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { Translate } from "../utils/ExtendedPageData";

export default function PathingPage() {
    const { config, saveConfig, error } = useConfig();

    if (error) return <div style={{ padding: "20px", color: "red" }}>Error: {error}</div>;
    if (!config) return <div style={{ padding: "20px" }}>Loading...</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("pathing.title")}</h2>
                <p>{Translate("pathing.description")}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">⛄</div>
                    <div>
                        <h3>{Translate("pathing.snowman.title")}</h3>
                        <p>{Translate("pathing.snowman.description")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("pathing.snowman.enable_path_label")}
                    checked={config.enable_snowman_path || false}
                    onChange={(val) => updateConfig("enable_snowman_path", val)}
                />

                {config.enable_snowman_path && (
                    <div className="form-group" style={{ marginTop: "12px" }}>
                        <label className="form-label">{Translate("common.repeats.item_usage_duration",[{from:"common.time",to:Translate("common.time.minutes")}])}</label>
                        <input
                            className="form-input"
                            value={config.snowman_claim_interval || "15"}
                            onChange={(e) => updateConfig("snowman_claim_interval", e.target.value)}
                            style={{ width: "80px" }}
                        />
                    </div>
                )}
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">🗺️</div>
                    <div>
                        <h3>{Translate("pathing.navigation_settings.title")}</h3>
                        <p>{Translate("pathing.navigation_settings.description")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("pathing.navigation_settings.reset_on_rare_label")}
                    description={Translate("pathing.navigation_settings.reset_on_rare_description")}
                    checked={config.reset_on_rare || false}
                    onChange={(val) => updateConfig("reset_on_rare", val)}
                />

                <ToggleSwitch
                    label={Translate("calibration.mouse_action_req.other.tele_back_limbo")}
                    description={Translate("calibration.mouse_action_req.other.tele_back_limbo_description")}
                    checked={config.teleport_back_to_limbo || false}
                    onChange={(val) => updateConfig("teleport_back_to_limbo", val)}
                />
            </div>
        </>
    );
}
