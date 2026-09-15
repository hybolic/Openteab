import { useEffect, useState } from "react";
import { Translate, openteab, PageIcons} from "../utils/ExtendedPageData";

export default function DonationsPage() {
    const [donators, setDonators] = useState<string>("Loading appreciation list...");
    useEffect(() => {
        fetch(openteab.donations.url)
            .then(res => res.text())
            .then(text => setDonators(text))
            .catch(err => setDonators("Unable to load appreciation list.\n" + err));
    }, []);

    return (
        <>
            <div className="page-header">
                <h2>{Translate("nav.donations")}</h2>
                <p>{Translate("donate.description")}</p>
            </div>

            <div className="card">
                <div className="card-header">
                    <div className="card-icon">{PageIcons.SupportUs}</div>
                    <div>
                        <h3>{Translate("credits.support")}</h3>
                        <p>{Translate("donate.help_project")}</p>
                    </div>
                </div>

                <div style={{ padding: "0 15px 15px 15px", color: "var(--text-secondary)", lineHeight: "1.6" }}>
                    <p style={{ marginBottom: "12px" }}>
                        {Translate("donate.p1")}
                    </p>
                    <p style={{ marginBottom: "12px" }}>
                        {Translate("donate.p2")}
                    </p>
                    <p style={{ marginBottom: "15px" }}>
                        {Translate("donate.p3")}
                    </p>

                    <a
                        href={openteab.donations.link}
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
                        {Translate("donate.gamepass_store")}
                    </a>
                    <div style={{ textAlign: "center", marginTop: "8px", fontSize: "12px", opacity: 0.7 }}>
                        {openteab.donations.link}
                    </div>
                </div>
            </div>

            <div className="card" style={{ flex: 1, display: "flex", flexDirection: "column", minHeight: "300px" }}>
                <div className="card-header">
                    <div className="card-icon">{PageIcons.Donator}</div>
                    <div>
                        <h3>{Translate("credits.donators")}</h3>
                        <p>{Translate("donate.donator_update")}</p>
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