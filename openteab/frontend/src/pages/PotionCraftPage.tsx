import { useState, useEffect, useRef } from "react";
import ToggleSwitch from "../components/ToggleSwitch";
import { Translate } from "../utils/ExtendedPageData";

export default function PotionCraftPage() {
    // State
    const [enableCrafting, setEnableCrafting] = useState(false);
    const [selectedPotion, setSelectedPotion] = useState("");
    const [potionFiles, setPotionFiles] = useState<string[]>([]);

    // Switching Logic
    const [enableSwitching, setEnableSwitching] = useState(false);
    const [switchInterval, setSwitchInterval] = useState(60);
    const [potion1, setPotion1] = useState("");
    const [potion2, setPotion2] = useState("");
    const [potion3, setPotion3] = useState("");
    const saveQueueRef = useRef<Promise<void>>(Promise.resolve());
    const configSnapshotRef = useRef<any>(null);

    useEffect(() => {
        refreshFiles();
        loadConfig();
    }, []);

    const refreshFiles = async () => {
        try {
            if (window.pywebview && window.pywebview.api) {
                const files = await window.pywebview.api.list_potion_files();
                setPotionFiles(files);
            }
        } catch (e) {
            console.error("Failed to list files:", e);
        }
    };

    const loadConfig = async () => {
        try {
            if (window.pywebview && window.pywebview.api) {
                const config: any = await window.pywebview.api.get_config();
                if (config) {
                    configSnapshotRef.current = config;
                    if (typeof config.enable_potion_crafting === 'boolean') setEnableCrafting(config.enable_potion_crafting);
                    setSelectedPotion(config.selected_potion_file ?? "");
                    if (typeof config.enable_potion_switching === 'boolean') setEnableSwitching(config.enable_potion_switching);
                    setSwitchInterval(Number(config.potion_switch_interval ?? 60));
                    setPotion1(config.potion_file_1 ?? "");
                    setPotion2(config.potion_file_2 ?? "");
                    setPotion3(config.potion_file_3 ?? "");
                }
            }
        } catch (e) {
            console.error("Failed to load config:", e);
        }
    };

    const saveConfig = (key: string, value: any) => {
        saveQueueRef.current = saveQueueRef.current
            .then(async () => {
                if (window.pywebview && window.pywebview.api) {
                    const baseConfig: any = configSnapshotRef.current ?? await window.pywebview.api.get_config();
                    const newConfig = { ...(baseConfig || {}), [key]: value };
                    configSnapshotRef.current = newConfig;
                    await window.pywebview.api.save_config(newConfig);
                }
            })
            .catch((e) => {
                console.error("Failed to save config:", e);
            });
    };

    // Generic handler to update state and save config
    const handleNumberChange = (val: string) => {
        const num = parseInt(val) || 0;
        setSwitchInterval(num);
        saveConfig("potion_switch_interval", num);
    };

    const openRecorder = async () => {
        try {
            if (window.pywebview?.api) {
                await window.pywebview.api.open_recorder_window_potion();
            }
        } catch (e) {
            console.error(e);
        }
    };

    // UI Helpers
    const PotionDropdown = ({ value, onChange, placeholder }: any) => (
        <div style={{ position: "relative", width: "100%" }}>
            <select
                className="form-input"
                style={{ width: "100%" }}
                value={value}
                onChange={(e) => onChange(e.target.value)}
            >
                <option value="">{placeholder}</option>
                {potionFiles.map(f => (
                    <option key={f} value={f}>{f}</option>
                ))}
            </select>
        </div>
    );

    return (
        <div className="animate-fade-in">
            <div className="page-header">
                <h2>{Translate("nav.potion_crafting")}</h2>
                <p>{Translate("potion_craft.description")}</p>
            </div>

            {/* Corner Borders container style similar to Obby */}
            <div style={{ position: "relative", border: "1px solid var(--border-color)", padding: "20px", marginBottom: "20px", background: "var(--card-bg)" }}>
                <div className="corner-bracket tl"></div>
                <div className="corner-bracket tr"></div>
                <div className="corner-bracket bl"></div>
                <div className="corner-bracket br"></div>

                <div className="card-header">
                    <div className="card-icon">🧪</div>
                    <div>
                        <h3>{Translate("potion_crafting.autocraft.title")}</h3>
                        <p>{Translate("potion_crafting.autocraft.description")}</p>
                    </div>
                </div>

                <div style={{ marginBottom: "15px" }}>
                    <ToggleSwitch
                        label={Translate("potion_crafting.autocraft.enable_label")}
                        description={Translate("potion_crafting.autocraft.enable_description")}
                        checked={enableCrafting}
                        onChange={(v) => {
                            if (v && !selectedPotion) {
                                alert(Translate("common.alert.no_potion_recipe"));
                                return;
                            }
                            setEnableCrafting(v);
                            saveConfig("enable_potion_crafting", v);
                        }}
                    />
                </div>

                <div style={{ display: "flex", gap: "8px", alignItems: "center", marginBottom: "12px" }}>
                    <button className="btn btn-accent" onClick={openRecorder} style={{ fontSize: "12px", padding: "6px 12px" }}>
                        {Translate("potion_crafting.autocraft.open_recorder")}
                    </button>
                    <button className="btn" onClick={refreshFiles} style={{ fontSize: "12px", padding: "6px 12px", backgroundColor: "#374151", color: "white", border: "1px solid var(--border-color)" }}>
                        {Translate("common.refresh_files")}
                    </button>
                </div>

                <div className="form-group">
                    <label className="form-label">{Translate("potion_crafting.autocraft.selected_recipe")}</label>
                    <PotionDropdown
                        value={selectedPotion}
                        onChange={(v: string) => { setSelectedPotion(v); saveConfig("selected_potion_file", v); }}
                        placeholder={Translate("potion_crafting.autocraft.placeholder")}
                    />
                </div>
            </div>

            {/* Switching Section */}
            <div style={{ position: "relative", border: "1px solid var(--border-color)", padding: "20px", background: "var(--card-bg)" }}>
                <div className="corner-bracket tl"></div>
                <div className="corner-bracket tr"></div>
                <div className="corner-bracket bl"></div>
                <div className="corner-bracket br"></div>

                <div className="card-header">
                    <div className="card-icon">🔄</div>
                    <div>
                        <h3>{Translate("potion_crafting.switching.title")}</h3>
                        <p>{Translate("potion_crafting.switching.description")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("potion_crafting.switching.enable_label")}
                    description={Translate("potion_crafting.switching.enable_description")}
                    checked={enableSwitching}
                    onChange={(v) => { setEnableSwitching(v); saveConfig("enable_potion_switching", v); }}
                />

                <div className="form-group" style={{ marginTop: "15px" }}>
                    <label className="form-label">{Translate("common.repeats.switch_interval", [{ from: "common.time", to: Translate("common.time.seconds") }])}</label>
                    <input
                        type="number"
                        className="form-input"
                        value={switchInterval}
                        onChange={(e) => handleNumberChange(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">{Translate("potion_crafting.switching.select_potion_x", [{from:"count",to:1}])}</label>
                    <PotionDropdown
                        value={potion1}
                        onChange={(v: string) => { setPotion1(v); saveConfig("potion_file_1", v); }}
                        placeholder={Translate("potion_crafting.switching.placeholder")}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">{Translate("potion_crafting.switching.select_potion_x", [{from:"count",to:2}])}</label>
                    <PotionDropdown
                        value={potion2}
                        onChange={(v: string) => { setPotion2(v); saveConfig("potion_file_2", v); }}
                        placeholder={Translate("potion_crafting.switching.placeholder")}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">{Translate("potion_crafting.switching.select_potion_x", [{from:"count",to:3}])}</label>
                    <PotionDropdown
                        value={potion3}
                        onChange={(v: string) => { setPotion3(v); saveConfig("potion_file_3", v); }}
                        placeholder={Translate("potion_crafting.switching.placeholder")}
                    />
                </div>

            </div>
        </div>
    );
}
