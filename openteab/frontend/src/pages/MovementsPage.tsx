import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { Translate, PageIcons } from "../utils/ExtendedPageData";

export default function MovementsPage() {
    const { config, saveConfig, error } = useConfig();

    if (error) return <div style={{ padding: "20px", color: "red" }}>{Translate("common.loading")}</div>;
    if (!config) return <div style={{ padding: "20px" }}>{Translate("common.loading")}</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("nav.movements")}</h2>
                <p>{Translate("movements.description")}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Movements}</div>
                    <div>
                        <h3>{Translate("movements.general_pathing")}</h3>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("movements.vip_label")}
                    description={Translate("movements.vip_description")}
                    checked={config.non_vip_movement_path || false}
                    onChange={(val) => updateConfig("non_vip_movement_path", val)}
                />

                <ToggleSwitch
                    label={Translate("movements.close_chat_label")}
                    description={Translate("movements.close_chat_description")}
                    checked={config.auto_chat_close || false}
                    onChange={(val) => updateConfig("auto_chat_close", val)}
                />
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Movements_obby}</div>
                    <div>
                        <h3>{Translate("movements.basic_obby")}</h3>
                    </div>
                </div>

                <div>
                    <ToggleSwitch
                        label={Translate("movements.obby.label")}
                        checked={config.enable_auto_obby || false}
                        onChange={async (val) => {
                            if (val) {
                                try {
                                    if (window.pywebview?.api) {
                                        const hasPath = await window.pywebview.api.check_obby_path_exists();
                                        if (!hasPath) {
                                            alert(Translate("common.alert.obby_path_not_found"));
                                            return;
                                        }
                                    }
                                } catch (e) {
                                    console.error("Failed to check obby path:", e);
                                }
                            }
                            updateConfig("enable_auto_obby", val);
                        }}
                    />

                    {config.enable_auto_obby && (
                        <div className="form-group" style={{ marginTop: "15px", marginLeft: "10px" }}>
                            <label className="form-label">{Translate("common.repeats.interval",[{from:"common.time",to:Translate("common.time.minutes")}])}</label>
                            <input
                                className="form-input"
                                type="number"
                                min="1"
                                value={config.auto_obby_interval || "15"}
                                onChange={(e) => updateConfig("auto_obby_interval", e.target.value)}
                                style={{ width: "80px" }}
                            />
                        </div>
                    )}

                    <div style={{ marginTop: "15px", borderTop: "1px solid var(--border-color)", paddingTop: "15px" }}>
                        <ToggleSwitch
                            label={Translate("movements.obby.float_label")}
                            checked={config.use_float_aura || false}
                            onChange={(val) => updateConfig("use_float_aura", val)}
                        />

                        {config.use_float_aura && (
                            <div className="form-group" style={{ marginTop: "10px", marginLeft: "10px" }}>
                                <label className="form-label">{Translate("movements.obby.aura_name")}</label>
                                <input
                                    className="form-input"
                                    type="text"
                                    value={config.float_aura_name || ""}
                                    onChange={(e) => updateConfig("float_aura_name", e.target.value)}
                                    placeholder={Translate("movements.obby.aura_placeholder")}
                                    style={{ width: "200px" }}
                                />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}