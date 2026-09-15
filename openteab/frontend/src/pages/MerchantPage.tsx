import { useConfig } from "../contexts/ConfigContext";
import ToggleSwitch from "../components/ToggleSwitch";
import { useEffect, useState } from "react";
import { PageIcons, Translate} from "../utils/ExtendedPageData";

interface MerchantItem {
    name: string;
    enabled: boolean;
    amount: number;
    stopAfterBuy: boolean; // mapped from 3rd boolean in array
    buyAll: boolean;
}

// Helper to parse config object to array
const parseItems = (itemsObj: any): MerchantItem[] => {
    if (!itemsObj) return [];
    return Object.entries(itemsObj).map(([name, val]: [string, any]) => ({
        name,
        enabled: val[0],
        amount: val[1],
        stopAfterBuy: false,
        buyAll: val.length > 3 ? !!val[3] : false
    }));
};

// Helper to convert array back to config object
const serializeItems = (items: MerchantItem[]): any => {
    const obj: any = {};
    items.forEach(item => {
        obj[item.name] = [item.enabled, item.amount, false, item.buyAll];
    });
    return obj;
};

function ItemTable({ items, onChange, accent }: {
    items: MerchantItem[];
    onChange: (items: MerchantItem[]) => void;
    accent: string;
}) {
    const toggle = (i: number, key: "enabled" | "stopAfterBuy" | "buyAll") => {
        const next = [...items];
        next[i] = { ...next[i], [key]: !next[i][key] };
        onChange(next);
    };
    const setAmount = (i: number, val: string) => {
        const next = [...items];
        const n = parseInt(val) || 1;
        next[i] = { ...next[i], amount: Math.max(1, n) };
        onChange(next);
    };

    return (
        <div className="item-table">
            <div className="item-table-header">
                <span className="item-col-name">{Translate("merchant.item_name")}</span>
                <span className="item-col-amount">{Translate("merchant.item_amount")}</span>
                <span style={{ width: "70px", textAlign: "center", fontSize: "12px" }}>{Translate("merchant.buy_all")}</span>
            </div>
            {items.map((item, i) => (
                <div key={item.name} className={`item-table-row ${item.enabled ? "item-row-active" : ""}`}>
                    <label className="item-col-name item-checkbox-label">
                        <input
                            type="checkbox"
                            checked={item.enabled}
                            onChange={() => toggle(i, "enabled")}
                            className="item-checkbox"
                            style={{ accentColor: accent }}
                        />
                        <span>{item.name}</span>
                    </label>
                    <input
                        type="number"
                        className="item-amount-input"
                        value={item.amount}
                        min={1}
                        disabled={item.buyAll}
                        onChange={(e) => setAmount(i, e.target.value)}
                        style={{ opacity: item.buyAll ? 0.4 : 1 }}
                    />
                    <div style={{ width: "70px", display: "flex", justifyContent: "center", alignItems: "center" }}>
                        <input
                            type="checkbox"
                            checked={item.buyAll}
                            onChange={() => toggle(i, "buyAll")}
                            className="item-checkbox"
                            style={{ accentColor: accent }}
                            title={Translate("merchant.max_buy_amount")}
                        />
                    </div>
                </div>
            ))}
        </div>
    );
}

export default function MerchantPage() {
    const { config, saveConfig, error } = useConfig();

    // Local state for items to avoid jitter, sync on change
    const [mariItems, setMariItems] = useState<MerchantItem[]>([]);
    const [jesterItems, setJesterItems] = useState<MerchantItem[]>([]);
    const [jesterExchangeItems, setJesterExchangeItems] = useState<MerchantItem[]>([]);
    const [rinItems, setRinItems] = useState<MerchantItem[]>([]);

    // Collapsible states (default collapsed for faster scrolling)
    const [mariOpen, setMariOpen] = useState(false);
    const [jesterOpen, setJesterOpen] = useState(false);
    const [jesterExchangeOpen, setJesterExchangeOpen] = useState(false);
    const [rinOpen, setRinOpen] = useState(false);

    useEffect(() => {
        if (config) {
            setMariItems(parseItems(config.Mari_Items));
            setJesterItems(parseItems(config.Jester_Items));

            const jesterExchangeDefaults = [
                "Icicle",
                "Wind Essence",
                "Rainy Bottle",
                "Stella's Star",
                "Hour Glass",
                "Eternal Flame",
                "Piece of Star",
                "Feather Vial",
                "Curruptaine",
                "NULL"
            ];
            let loadedJesterExchange = parseItems(config.Jester_Exchange_Items);
            jesterExchangeDefaults.forEach(name => {
                if (!loadedJesterExchange.find(i => i.name === name)) {
                    loadedJesterExchange.push({ name, enabled: false, amount: 1, stopAfterBuy: false, buyAll: false });
                }
            });
            setJesterExchangeItems(loadedJesterExchange);

            const rinDefaults = [
                "Sunstone Talisman",
                "Moonstone Talisman",
                "Day and Night Talisman",
                "Overtime Talisman",
                "Soul Collector's Talisman",
                "Soul Master's Talisman"
            ];

            let loadedRin = parseItems(config.Rin_Items);
            rinDefaults.forEach(name => {
                if (!loadedRin.find(i => i.name === name)) {
                    loadedRin.push({ name, enabled: false, amount: 1, stopAfterBuy: false, buyAll: false });
                }
            });
            setRinItems(loadedRin);
        }
    }, [config]);

    if (error) return <div style={{ padding: "20px", color: "red" }}>Error: {error}</div>;
    if (!config) return <div style={{ padding: "20px" }}>Loading...</div>;

    const updateConfig = (key: string, value: any) => {
        saveConfig({ ...config, [key]: value });
    };

    const handleMariChange = (items: MerchantItem[]) => {
        setMariItems(items);
        updateConfig("Mari_Items", serializeItems(items));
    };

    const handleJesterChange = (items: MerchantItem[]) => {
        setJesterItems(items);
        updateConfig("Jester_Items", serializeItems(items));
    };

    const handleJesterExchangeChange = (items: MerchantItem[]) => {
        setJesterExchangeItems(items);
        updateConfig("Jester_Exchange_Items", serializeItems(items));
    };

    const handleRinChange = (items: MerchantItem[]) => {
        setRinItems(items);
        updateConfig("Rin_Items", serializeItems(items));
    };

    const handleMerchantTeleporterToggle = (enabled: boolean) => {
        if (enabled && config.merchant_ocr) {
            alert("Please disable 'Detect merchant on chat (using OCR)' before enabling the Auto Merchant using Merchant Teleporter.");
            return;
        }
        updateConfig("merchant_teleporter", enabled);
    };

    const handleMerchantOcrToggle = (enabled: boolean) => {
        if (enabled && config.merchant_teleporter) {
            alert("Please disable 'Enable Auto Merchant (requires merchant teleporter)' before enabling merchant OCR detection.");
            return;
        }
        updateConfig("merchant_ocr", enabled);
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("merchant.merchant")}</h2>
                <p>{Translate("merchant.merchant_description")}</p>
            </div>

            {/* Merchant Settings */}
            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Merchant}</div>
                    <div>
                        <h3>{Translate("merchant.teleporter")}</h3>
                        <p>{Translate("merchant.teleporter_description")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("merchant.auto_merchant")}
                    description={Translate("merchant.auto_merchant_description")}
                    checked={config.merchant_teleporter || false}
                    onChange={handleMerchantTeleporterToggle}
                />
                {config.merchant_teleporter && (
                    <div className="duration-input" style={{ marginTop: "6px", marginBottom: "10px" }}>
                        <label className="form-label">{Translate("merchant.usage_duration")}:</label>
                        <input
                            className="form-input"
                            value={config.mt_duration || "1"}
                            onChange={(e) => updateConfig("mt_duration", e.target.value)}
                        />
                        <span className="unit">{Translate("common.min")}</span>
                    </div>
                )}

                <ToggleSwitch
                    label={Translate("merchant.merchant_ocr")}
                    description={Translate("merchant.merchant_ocr_description")}
                    checked={config.merchant_ocr || false}
                    onChange={handleMerchantOcrToggle}
                />
                {config.merchant_ocr && (
                    <div className="info-banner" style={{ marginTop: "10px", marginBottom: "10px" }}>
                        <strong>{Translate("merchant.merchant_ocr_reminder")}:</strong>{" "}{Translate("merchant.merchant_ocr_text")}
                        <div className="form-row" style={{ marginTop: "10px" }}>
                            <div className="form-group">
                                <label className="form-label">{Translate("merchant.merchant_ocr_interval")}</label>
                                <input
                                    className="form-input"
                                    type="number"
                                    value={config.merchant_ocr_interval ?? "60"}
                                    min="1"
                                    onChange={(e) => updateConfig("merchant_ocr_interval", e.target.value)}
                                    style={{ width: "90px" }}
                                />
                            </div>
                        </div>
                    </div>
                )}

                <ToggleSwitch
                    label={Translate("merchant.auto_limbo")}
                    description={Translate("merchant.auto_limbo_description")}
                    checked={config.auto_merchant_in_limbo || false}
                    onChange={(val) => updateConfig("auto_merchant_in_limbo", val)}
                />

                <div className="form-row" style={{ marginTop: "10px" }}>
                    <div className="form-group">
                        <label className="form-label">{Translate("merchant.extra_slot")}</label>
                        <p className="form-hint">{Translate("merchant.extra_slot_description")}</p>
                        <input
                            className="form-input"
                            value={config.merchant_extra_slot || "0"}
                            onChange={(e) => updateConfig("merchant_extra_slot", e.target.value)}
                            style={{ width: "70px" }}
                        />
                    </div>
                </div>
            </div>

            {/* Jester Exchange Settings */}
            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.JesterExchange}</div>
                    <div>
                        <h3>{Translate("merchant.jester_exchange")}</h3>
                        <p>{Translate("merchant.jester_exchange_description")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("merchant.enable_jester")}
                    checked={config.enable_jester_exchange || false}
                    onChange={(val) => updateConfig("enable_jester_exchange", val)}
                />
                
                {config.enable_jester_exchange && (
                    <div className="form-row" style={{ marginTop: "10px", marginBottom: "10px" }}>
                        <div className="form-group">
                            <label className="form-label">{Translate("merchant.jester_exchange_x")}</label>
                            <input
                                className="form-input"
                                type="number"
                                value={config.jester_exchange_threshold ?? "3"}
                                min="1"
                                onChange={(e) => updateConfig("jester_exchange_threshold", e.target.value)}
                                style={{ width: "90px" }}
                            />
                        </div>
                    </div>
                )}
                
                {config.enable_jester_exchange && (
                    <div style={{ marginTop: "15px" }}>
                        <div
                            className="card-header"
                            onClick={() => setJesterExchangeOpen(!jesterExchangeOpen)}
                            style={{ cursor: "pointer", userSelect: "none", padding: "10px", background: "rgba(0,0,0,0.1)", borderRadius: "6px" }}
                            title={Translate("common.click_to_toggle")}
                        >
                            <div style={{ flexGrow: 1 }}>
                                <h4>{Translate("merchant.select_items_to_exchange")}</h4>
                            </div>
                            <div style={{ fontSize: "1.2rem", color: "var(--text-secondary)", transform: jesterExchangeOpen ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
                                {PageIcons.DOWN}
                            </div>
                        </div>
                        {jesterExchangeOpen && <ItemTable items={jesterExchangeItems} onChange={handleJesterExchangeChange} accent="#10b981" />}
                    </div>
                )}
            </div>

            {/* Ping Settings */}
            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Ping}</div>
                    <div>
                        <h3>{Translate("webhook.discord_pings")}</h3>
                        <p>{Translate("merchant.notify_when_found")}</p>
                    </div>
                </div>

                <ToggleSwitch
                    label={Translate("merchant.ping_mari")}
                    description={Translate("webhook.custom_ping")}
                    checked={config.ping_mari || false}
                    onChange={(val) => updateConfig("ping_mari", val)}
                />
                {config.ping_mari && (
                    <div className="form-group" style={{ marginTop: "6px", marginBottom: "10px" }}>
                        <label className="form-label">{Translate("webhook.user_roleid")}</label>
                        <input
                            className="form-input"
                            value={config.mari_user_id || ""}
                            onChange={(e) => updateConfig("mari_user_id", e.target.value)}
                            placeholder="123456789012345678"
                            style={{ width: "240px" }}
                        />
                    </div>
                )}

                <ToggleSwitch
                    label={Translate("merchant.ping_jester")}
                    description={Translate("webhook.custom_ping")}
                    checked={config.ping_jester || false}
                    onChange={(val) => updateConfig("ping_jester", val)}
                />
                {config.ping_jester && (
                    <div className="form-group" style={{ marginTop: "6px", marginBottom: "10px" }}>
                        <label className="form-label">{Translate("webhook.user_roleid")}</label>
                        <input
                            className="form-input"
                            value={config.jester_user_id || ""}
                            onChange={(e) => updateConfig("jester_user_id", e.target.value)}
                            placeholder="123456789012345678"
                            style={{ width: "240px" }}
                        />
                    </div>
                )}

                <ToggleSwitch
                    label={Translate("merchant.ping_rin")}
                    description={Translate("webhook.custom_ping")}
                    checked={config.ping_rin || false}
                    onChange={(val) => updateConfig("ping_rin", val)}
                />
                {config.ping_rin && (
                    <div className="form-group" style={{ marginTop: "6px", marginBottom: "10px" }}>
                        <label className="form-label">{Translate("webhook.user_roleid")}</label>
                        <input
                            className="form-input"
                            value={config.rin_user_id || ""}
                            onChange={(e) => updateConfig("rin_user_id", e.target.value)}
                            placeholder="123456789012345678"
                            style={{ width: "240px" }}
                        />
                    </div>
                )}
            </div>

            {/* Mari stuff*/}
            <div className="card">
                <div
                    className="card-header"
                    onClick={() => setMariOpen(!mariOpen)}
                    style={{ cursor: "pointer", userSelect: "none" }}
                    title={Translate("common.click_to_toggle")}
                >
                    <div className="card-icon">{PageIcons.Mari}</div>
                    <div style={{ flexGrow: 1 }}>
                        <h3>{Translate("merchant.item_settings",[{from:"merchant",to:"Mari"}])}</h3>
                        <p>{Translate("merchant.autopurchase_select_items",[{from:"merchant",to:"Mari"}])}</p>
                    </div>
                    <div style={{ fontSize: "1.2rem", color: "var(--text-secondary)", transform: mariOpen ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
                        {PageIcons.DOWN}
                    </div>
                </div>
                {mariOpen && <ItemTable items={mariItems} onChange={handleMariChange} accent="#7c5bf5" />}
            </div>

            {/* Jester stuffs */}
            <div className="card">
                <div
                    className="card-header"
                    onClick={() => setJesterOpen(!jesterOpen)}
                    style={{ cursor: "pointer", userSelect: "none" }}
                    title={Translate("common.click_to_toggle")}
                >
                    <div className="card-icon">{PageIcons.Jester}</div>
                    <div style={{ flexGrow: 1 }}>
                        <h3>{Translate("merchant.item_settings",[{from:"merchant",to:"Jester"}])}</h3>
                        <p>{Translate("merchant.autopurchase_select_items",[{from:"merchant",to:"Jester"}])}</p>
                    </div>
                    <div style={{ fontSize: "1.2rem", color: "var(--text-secondary)", transform: jesterOpen ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
                        {PageIcons.DOWN}
                    </div>
                </div>
                {jesterOpen && <ItemTable items={jesterItems} onChange={handleJesterChange} accent="#f59e0b" />}
            </div>

            {/* Rin stuff*/}
            <div className="card">
                <div
                    className="card-header"
                    onClick={() => setRinOpen(!rinOpen)}
                    style={{ cursor: "pointer", userSelect: "none" }}
                    title={Translate("common.click_to_toggle")}
                >
                    <div className="card-icon">{PageIcons.Rin}</div>
                    <div style={{ flexGrow: 1 }}>
                        <h3>{Translate("merchant.item_settings",[{from:"merchant",to:"Rin"}])}</h3>
                        <p>{Translate("merchant.autopurchase_select_items",[{from:"merchant",to:"Rin"}])}</p>
                    </div>
                    <div style={{ fontSize: "1.2rem", color: "var(--text-secondary)", transform: rinOpen ? "rotate(180deg)" : "rotate(0deg)", transition: "transform 0.2s" }}>
                        {PageIcons.DOWN}
                    </div>
                </div>
                {rinOpen && <ItemTable items={rinItems} onChange={handleRinChange} accent="#06b6d4" />}
            </div>
        </>
    );
}