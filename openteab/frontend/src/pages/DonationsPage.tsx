import { useEffect, useState } from "react";
import { type ExtendedProperties, PageIcons} from "../utils/ExtendedPageData";

export default function DonationsPage({langData}:ExtendedProperties) {
    const [donators, setDonators] = useState<string>("Loading appreciation list...");
    if(!langData)return
    useEffect(() => {
        fetch("https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/appreciation_list.txt")
            .then(res => res.text())
            .then(text => setDonators(text))
            .catch(err => setDonators("Unable to load appreciation list.\n" + err));
    }, []);

    return (
        <>
            <div className="page-header">
                <h2>{langData.nav.donations}</h2>
                <p>{langData.donate.description}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.SupportUs}</div>
                    <div>
                        <h3>{langData.credits.support}</h3>
                        <p>{langData.donate.help_project}</p>
                    </div>
                </div>

                <div style={{ padding: "0 15px 15px 15px", color: "var(--text-secondary)", lineHeight: "1.6" }}>
                    <p style={{ marginBottom: "12px" }}>
                        {langData.donate.p1}
                    </p>
                    <p style={{ marginBottom: "12px" }}>
                        {langData.donate.p2}
                    </p>
                    <p style={{ marginBottom: "15px" }}>
                        {langData.donate.p3}
                    </p>

                    <a
                        href="https://www.roblox.com/games/18203398779/Medival-castle#!/store"
                        target="_blank"
                        rel="noreferrer"
                        className="btn btn-accent"
                        style={{
                            width: "100%",
                            justifyContent: "center",
                            fontWeight: "bold",
                            textDecoration: "none",
                            display: "flex",
                            alignItems: "center"
                        }}
                    >
                        {langData.donate.gamepass_store}
                    </a>
                    <div style={{ textAlign: "center", marginTop: "8px", fontSize: "12px", opacity: 0.7 }}>
                        https://www.roblox.com/games/18203398779/Medival-castle#!/store
                    </div>
                </div>
            </div>

            <div className="card" style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: "300px" }}>
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Donator}</div>
                    <div>
                        <h3>{langData.credits.donators}</h3>
                        <p>{langData.donate.donator_update}</p>
                    </div>
                </div>

                <div style={{ padding: "15px", flex: 1, display: "flex", flexDirection: "column" }}>
                    <textarea
                        readOnly
                        value={donators}
                        style={{
                            flex: 1,
                            width: "100%",
                            resize: "none",
                            backgroundColor: "rgba(0,0,0,0.2)",
                            color: "var(--text-primary)",
                            border: "1px solid var(--border-color)",
                            borderRadius: "8px",
                            padding: "12px",
                            fontFamily: "monospace",
                            fontSize: "13px",
                            lineHeight: "1.5",
                            outline: "none"
                        }}
                    />
                </div>
            </div>
        </>
    );
}