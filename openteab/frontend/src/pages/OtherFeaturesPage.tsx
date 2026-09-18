import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { Translate } from "../utils/ExtendedPageData";

export default function OtherFeaturesPage() {
    const { config, saveConfig, error } = useConfig();

    if (error) return <div style={{ padding: "20px", color: "red" }}>Error: {error}</div>;
    if (!config) return <div style={{ padding: "20px" }}>Loading...</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("nav.other_features")}</h2>
                <p>{Translate("other_features.description")}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">⚡</div>
                    <div>
                        <h3>{Translate("other_features.rare_biome_actions.title")}</h3>
                        <p>{Translate("other_features.rare_biome_actions.description")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("other_features.rare_biome_actions.enable_label")}
                    description={Translate("other_features.rare_biome_actions.enable_description")}
                    checked={config.enable_buff_glitched || false}
                    onChange={(val) => updateConfig("enable_buff_glitched", val)}
                />

                <ToggleSwitch
                    label={Translate("other_features.rare_biome_actions.reset_character_label")}
                    description={Translate("other_features.rare_biome_actions.reset_character_description")}
                    checked={config.reset_on_rare || false}
                    onChange={(val) => updateConfig("reset_on_rare", val)}
                />

                <ToggleSwitch
                    label={Translate("other_features.rare_biome_actions.teleport_back_to_limbo_label")}
                    description={Translate("other_features.rare_biome_actions.teleport_back_to_limbo_description")}
                    checked={config.teleport_back_to_limbo || false}
                    onChange={(val) => updateConfig("teleport_back_to_limbo", val)}
                />
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">🛠️</div>
                    <div>
                        <h3>{Translate("other_features.system_settings.title")}</h3>
                        <p>{Translate("other_features.system_settings.description")}</p>
                    </div>
                </div>

                <div className="setting-row" style={{ padding: '15px 20px', borderBottom: '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <div style={{ fontWeight: 600, color: 'var(--text-bright)' }}>{Translate("settings.open_appdata")}</div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{Translate("settings.open_appdata_description")}</div>
                    </div>
                    <button 
                        className="btn primary" 
                        onClick={() => window.pywebview?.api?.open_appdata()}
                        style={{ padding: '8px 16px', borderRadius: '4px', cursor: 'pointer', backgroundColor: 'var(--primary)', color: 'white', border: 'none', fontWeight: 600 }}
                    >
                        {Translate("common.open_folder")}
                    </button>
                </div>

                <ToggleSwitch
                    label={Translate("other_features.rare_biome_actions.glitched_visual_label")}
                    description={<span style={{ color: "red", fontWeight: "bold" }}>{Translate("other_features.rare_biome_actions.glitched_visual_description")}</span>}
                    checked={config.enable_glitch_effect || false}
                    onChange={(val) => updateConfig("enable_glitch_effect", val)}
                />

                <ToggleSwitch
                    label={Translate("settings.antiAfk")}
                    description={Translate("other_features.rare_biome_actions.prevent_disconnect")}
                    checked={config.anti_afk || false}
                    onChange={(val) => updateConfig("anti_afk", val)}
                />

                <div className="setting-row" style={{ padding: '0 20px 20px 20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>{Translate("common.repeats.item_usage_duration",[{from:"common.time",to:Translate("common.time.minutes")}])}</span>
                    <input 
                        type="number" 
                        className="form-input" 
                        style={{ width: '80px', textAlign: 'center' }}
                        value={config.anti_afk_interval || "5"}
                        min="1"
                        max="20"
                        onChange={(e) => updateConfig("anti_afk_interval", e.target.value)}
                    />
                </div>

                <ToggleSwitch
                    label={Translate("settings.autoupdate_label")}
                    description={Translate("settings.autoupdate_description")}
                    checked={config.auto_update_enabled !== false}
                    onChange={(val) => updateConfig("auto_update_enabled", val)}
                />

                <ToggleSwitch
                    label={Translate("settings.idlemode_label")}
                    description={Translate("settings.idlemode_description")}
                    checked={config.enable_idle_mode || false}
                    onChange={(val) => updateConfig("enable_idle_mode", val)}
                />

                <ToggleSwitch
                    label={Translate("other_features.make_roblox_instance_on_label")}
                    description={Translate("other_features.make_roblox_instance_on_description")}
                    checked={config.auto_roblox_fullscreen || false}
                    onChange={(val) => updateConfig("auto_roblox_fullscreen", val)}
                />

                <ToggleSwitch
                    label={Translate("settings.azerty_keyboard_mode_experimental_label")}
                    description={Translate("settings.azerty_keyboard_mode_experimental_description")}
                    checked={config.azerty_mode || false}
                    onChange={(val) => updateConfig("azerty_mode", val)}
                />
            </div>
        </>
    );
}