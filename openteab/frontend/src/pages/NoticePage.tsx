import { useState, useEffect } from "react";
import React from "react";
import { Translate, openteab } from "../utils/ExtendedPageData";

export default function NoticePage() {
    const [content, setContent] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(openteab.notice_tab_contents)
            .then(res => res.text())
            .then(text => {
                setContent(text);
                setLoading(false);
            })
            .catch(err => {
                console.error("Failed to fetch notice:", err);
                setLoading(false);
            });
    }, []);

    const parseNotice = (text: string) => {
        const lines = text.split("\n");
        const elements: React.ReactNode[] = [];
        let currentList: React.ReactNode[] = [];
        let currentTitle: string | null = null;

        const flushSection = (key: number) => {
            if (currentTitle || currentList.length > 0) {
                elements.push(
                    <div key={key} className="changelog-item">
                        {currentTitle && <h4>{currentTitle}</h4>}
                        {currentList.length > 0 && <ul>{currentList}</ul>}
                    </div>
                );
                currentList = [];
                currentTitle = null;
            }
        };

        lines.forEach((line, i) => {
            const trimmed = line.trim();
            if (!trimmed) return;

            if (trimmed.startsWith("# ")) {
                flushSection(i);
                currentTitle = trimmed.substring(2);
            } else if (trimmed.startsWith("## ")) {
                currentList.push(<li key={i} style={{ listStyle: "none", fontWeight: 700, marginLeft: "-1em", marginTop: "8px" }}>{trimmed.substring(3)}</li>);
            } else if (trimmed.startsWith("- ")) {
                currentList.push(<li key={i}>{trimmed.substring(2)}</li>);
            } else if (trimmed.startsWith("PLEASE WATCH")) {
            } else {
                currentList.push(<li key={i} style={{ listStyle: "none" }}>{trimmed}</li>);
            }
        });

        flushSection(lines.length);
        return elements;
    };

    return (
        <>
            <div className="page-header">
                <h2>{Translate("nav.notice")}</h2>
                <p>{Translate("notice.description")}</p>
            </div>

            <div className="info-banner">
                {Translate("notice.new_to_macro")}
            </div>

            {loading ? (
                <div style={{ padding: "20px", textAlign: "center", color: "var(--text-muted)" }}>
                    {Translate("common.loading")}
                </div>
            ) : content ? (
                parseNotice(content)
            ) : (
                <div style={{ padding: "20px", textAlign: "center", color: "var(--text-danger)" }}>
                    {Translate("common.alert.failed_to_load_notice")}
                </div>
            )}

            <div className="info-banner" style={{ marginTop: "16px" }}>
                {Translate("notice.updates_link")}
            </div>
        </>
    );
}