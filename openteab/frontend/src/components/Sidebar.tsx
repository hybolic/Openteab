interface SidebarProps {
    activeTab: string;
    onTabChange: (tab: string) => void;
    isGlitching: boolean;
    macroVersion: string;
}
import GlitchOverlay from "./GlitchOverlay";
import { useGlitchText } from "../hooks/useGlitchText";
import { Translate } from "../utils/ExtendedPageData";

export default function Sidebar({ activeTab, onTabChange, isGlitching, macroVersion }: SidebarProps) {
    

    const SidebarItem = ({ item, isActive, onClick, isGlitching, locked }: { item: any; isActive: boolean; onClick: () => void; isGlitching: boolean; locked?: boolean }) => {
        const label = useGlitchText(item.label || "", isGlitching);
        const isDisabled = item.disabled || locked;
        return (
            <div
                className={`sidebar-item ${isActive ? "active" : ""}`}
                onClick={() => !isDisabled && onClick()}
                style={isDisabled ? { opacity: 0.3, cursor: "not-allowed", pointerEvents: "none" } : {}}
                title={locked ? "🔒 Locked" : undefined}
            >
                <span className="icon">{locked ? "🔒" : item.icon}</span>
                {label}
                {item.disabled && <span style={{ fontSize: "10px", marginLeft: "auto", opacity: 0.7 }}>(WIP)</span>}
            </div>
        );
    };

    const navItems = [
        { section: Translate("nav.section.general") },
        { id: "notice", label: Translate("nav.notice"), icon: "📋" },
        { id: "webhook", label: Translate("nav.webhook"), icon: "🔗" },
        { id: "stats", label: Translate("nav.stats"), icon: "📊" },
        { id: "status", label: Translate("nav.status"), icon: "⚙️" },
        { section: Translate("nav.section.macro_settings") },
        { id: "misc", label: Translate("nav.automated_actions"), icon: "🤖" },
        { id: "calibrations", label: Translate("nav.macro_calibrations"), icon: "🎯" },
        { id: "remoteaccess", label: Translate("nav.remote_control"), icon: "🔑" },
        { section: Translate("nav.section.main_features") },
        { id: "fishing", label: Translate("nav.fishing"), icon: "🎣" },
        { id: "merchant", label: Translate("nav.merchant"), icon: "🎭" },
        { id: "autopopbuff", label: Translate("nav.auto_pop_buff"), icon: "🧪" },
        { id: "auras", label: Translate("nav.auras"), icon: "✨" },
        { id: "movements", label: Translate("nav.movements"), icon: "🗺️" },
        { id: "potioncraft", label: Translate("nav.potion_crafting"), icon: "🧪" },
        { id: "otherfeatures", label: Translate("nav.other_features"), icon: "🔧" },
        { id: "customization", label: Translate("nav.customizations"), icon: "🔧" },
        { section: Translate("nav.section.others") },
        { id: "credits", label: Translate("nav.credits"), icon: "💜" },
        { id: "donations", label: Translate("nav.donations"), icon: "💎" },
    ];

    const title = useGlitchText("Openteab Macro", isGlitching);
    const version = useGlitchText(macroVersion || "v?.?.?", isGlitching);

    return (
        <div className="sidebar" style={{ position: "relative" }}>
            {isGlitching && <GlitchOverlay />}
            <div className="sidebar-brand">
                <h1>{title}</h1>
                <div className="version">{version}</div>
            </div>

            <div className="sidebar-nav">
                {navItems.map((item, i) => {
                    if ("section" in item && item.section) {
                        return (
                            <div key={`s-${i}`} className="sidebar-section-label">
                                {item.section}
                            </div>
                        );
                    }
                    return (
                        <SidebarItem
                            key={item.id}
                            item={item}
                            isActive={activeTab === item.id}
                            onClick={() => item.id && onTabChange(item.id)}
                            isGlitching={isGlitching}
                        />
                    );
                })}
            </div>

            <div className="sidebar-footer">
                <div className="by-line">
                    <div>Coteab Macro made by <br/><span>Coteab Development Team</span></div>
                    <div>Openteab Maintained by <br/><span style={{color:"#ed27ff"}}>The Community</span>{" and "}<span style={{color:"#ffa227"}}>Nadir</span>{" "}{Translate("sidebar.nadirhype")}</div>
                </div>
            </div>
        </div>
    );
}