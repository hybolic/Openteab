import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { looksLikeWebhookUrl, getWebhookWarning } from "../utils/webhookGuard";
import { Translate } from "../utils/ExtendedPageData";

export default function RemoteAccessPage() {
    const { config, saveConfig, error } = useConfig();

    if (error) return <div style={{ padding: "20px", color: "red" }}>Error: {error}</div>;
    if (!config) return <div style={{ padding: "20px" }}>Loading...</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    const handleBotTokenChange = (val: string) => {
        if (looksLikeWebhookUrl(val)) {
            alert(getWebhookWarning(val, "Discord Bot Token"));
            return;
        }
        updateConfig("remote_bot_token", val);
    };

    const handleUserIdChange = (val: string) => {
        if (looksLikeWebhookUrl(val)) {
            alert(getWebhookWarning(val, "Allowed User ID"));
            return;
        }
        updateConfig("remote_allowed_user_id", val);
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("remote_access.title")}</h2>
                <p>{Translate("remote_access.description")}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">🔑</div>
                    <div>
                        <h3>{Translate("remote.access_control")}</h3>
                        <p>{Translate("remote_access.enable_and_configure_remote")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("remote_access.enable_remote_access_control_label")}
                    checked={config.remote_access_enabled || false}
                    onChange={(val) => updateConfig("remote_access_enabled", val)}
                />

                {config.remote_access_enabled && (
                    <div style={{ marginTop: "12px", display: "flex", flexDirection: "column", gap: "12px" }}>
                        <div className="form-group">
                            <label className="form-label">{Translate("remote_access.discord_bot_token")}</label>
                            <input
                                className="form-input"
                                type="password"
                                value={config.remote_bot_token || ""}
                                onChange={(e) => handleBotTokenChange(e.target.value)}
                                placeholder={Translate("remote_access.enter_your_discord_bot")}
                                style={{ width: "100%", maxWidth: "440px" }}
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label">{Translate("remote_access.allowed_user_id")}</label>
                            <input
                                className="form-input"
                                value={config.remote_allowed_user_id || ""}
                                onChange={(e) => handleUserIdChange(e.target.value)}
                                placeholder="123456789012345678"
                                style={{ width: "220px" }}
                            />
                        </div>

                        <div>
                            <a
                                href="https://www.youtube.com/watch?v=s2S7Bncx9ns"
                                target="_blank"
                                rel="noreferrer"
                                style={{
                                    color: "royalblue",
                                    textDecoration: "underline",
                                    cursor: "pointer",
                                    fontSize: "13px",
                                }}
                            >
                                {Translate("settings.setup_tutorial")}
                            </a>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}