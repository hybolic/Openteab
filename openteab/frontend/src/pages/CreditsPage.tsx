import type { ExtendedProperties } from "../utils/ExtendedPageData";

export default function CreditsPage({langData,creditsData}: ExtendedProperties) {

    if (!creditsData || !langData) {
        return <div>Loading...</div>;
    }
    const credits = creditsData.credits;
    const credits_lang = langData.credits.credits;

    return (
        <>
            {/* Developers Card */}
            <div className="page-header">
                <h2>{credits_lang?.current_developers?.title ?? credits.current_developers.title}</h2>
                <p>{credits_lang?.current_developers?.description ?? credits.current_developers.description}</p>
            </div>

            <div className="card">
                <div style={{ display: "flex", justifyContent: "center", marginBottom: "16px" }}>
                    <img
                        src={credits.current_developers.members[0].avatarUrl}
                        alt="Current Maintainer"
                        style={{
                            width: "80px",
                            height: "auto",
                            borderRadius: "8px",
                            border: "1px solid var(--border)",
                            boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                            background: "rgba(128, 0, 255, 1)"
                        }}
                        onError={(e) => e.currentTarget.src = credits.current_developers.members[0].backupUrl }
                    />
                </div>

                <div className="credits-list">
                    <div className="credit-item">
                        <div className="credit-avatar">V</div>
                        <div className="credit-info">
                            <ul style={{ margin: 0, paddingLeft: "16px", listStyle: "disc" }}>
                                {
                                credits.current_developers.members.map((member: any, index:number) => {
                                    const link = credits.current_developers.links.find(
                                        (link: any) => link.name === member.name
                                    );

                                    return (
                                        <li key={member.name}>
                                            <strong>
                                                {link ? (
                                                    <a href={link.url} target="_blank" rel="noreferrer" title={link.label}>
                                                        {member.name}
                                                    </a>
                                                ) : (
                                                    member.name
                                                )}
                                            </strong> ({credits_lang?.current_developers?.members[index]?.role ?? member.role})
                                        </li>
                                    );
                                })}
                            </ul>
                        </div>
                    </div>
                </div>

                <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px", marginTop: "16px" }}>
                    {credits.current_developers.links.map((link: any, index:number) => (
                        <a key={link.url} href={link.url} target="_blank" rel="noreferrer" style={{ color: "var(--accent)", fontSize: "13px" }}>
                            {credits_lang?.current_developers?.links[index]?.label ?? link.label}
                        </a>
                    ))}
                </div>
            </div>


            <div className="page-header" style={{textAlign: "center"}}>
                <h1>{credits_lang?.original_developers?.title ?? credits.original_developers.title}</h1>
                <h2>{credits_lang?.original_developers?.subtitle ?? credits.original_developers.subtitle}</h2>
                <h2><strong>{credits.original_developers.projectName}</strong></h2>
            </div>

            {/* Developers Card */}
            <div className="card">
                <div style={{ display: "flex", justifyContent: "center", marginBottom: "16px" }}>
                    <img
                        src={credits.original_developers.imageUrl}
                        alt="Old Dev Team"
                        style={{
                            width: "300px",
                            height: "auto",
                            borderRadius: "8px",
                            border: "1px solid var(--border)",
                            boxShadow: "0 4px 6px rgba(0,0,0,0.1)"
                        }}
                        onError={(e) => e.currentTarget.src = credits.original_developers.backupUrl }
                    />
                </div>

                <div className="credits-list">
                    <div className="credit-item">
                        <div className="credit-avatar heart-avatar">&#10084;</div>
                        <div className="credit-info">
                            <ul style={{ margin: 0, paddingLeft: "16px", listStyle: "disc" }}>
                                {credits.original_developers.members.map((member: any, index:number) => (
                                    <li key={member.name}>
                                        <strong>{member.name}</strong> ({credits_lang?.original_developers?.members[index]?.role ?? member.role})
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>

                <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "8px", marginTop: "16px" }}>
                    {credits.original_developers.links.map((link: any, index:number) => (
                        <a key={link.url} href={link.url} target="_blank" rel="noreferrer"
                            style={{ color: "var(--accent)", textDecoration: "underline" }}>
                            {credits_lang?.original_developers?.links[index]?.label ?? link.label}
                        </a>
                    ))}
                </div>
            </div>

            {/* Inspired By Card */}
            <div className="card" style={{ textAlign: "center" }}>
                {credits.inspiration.map((person: any, index:number) => (
                    <div key={person.name}>
                        <div style={{ display: "flex", justifyContent: "center", marginBottom: "12px" }}>
                            <img
                                src={person.avatarUrl}
                                alt={person.name}
                                style={{
                                    width: "120px",
                                    height: "auto",
                                    objectFit: "cover",
                                    borderRadius: "8px",
                                    border: "1px solid var(--border)"
                                }}
                                onError={(e) => e.currentTarget.src = person.backupUrl }
                            />
                        </div>

                        <h3>{credits_lang?.inspiration[index]?.title ?? person.title}: {person.name}</h3>

                        {person.links.map((link: any, index2:number) => (
                            <p key={link.url}>
                                <a href={link.url} target="_blank" rel="noreferrer"
                                    style={{ color: "var(--accent)", textDecoration: "underline", cursor: "pointer" }}>
                                    {credits_lang?.inspiration[index]?.links[index2].label ?? link.label}
                                </a>
                            </p>
                        ))}
                    </div>
                ))}
            </div>

            {/* Extra Credits */}
            <div className="card">
                <div className="card-header">
                    <div className="card-icon">🏅</div>
                    <div>
                        <h3>{credits_lang?.extra_credits?.title ?? credits.extra_credits.title}</h3>
                        <p>{credits_lang?.extra_credits?.description ?? credits.extra_credits.description}</p>
                    </div>
                </div>

                <div style={{
                    padding: "14px 16px",
                    background: "var(--bg-input)",
                    border: "1px solid var(--border)",
                    borderRadius: "var(--radius-md)",
                    fontSize: "13px",
                    lineHeight: "1.8",
                    color: "var(--text-secondary)",
                }}>
                    {credits.extra_credits.credits.map((credit: any, index:number) => {
                        const link = credit.links?.[0];

                        return (
                            <div key={credit.name}>
                                - {link ? (
                                    <a href={link.url} target="_blank" rel="noreferrer" title={link.label}>
                                        {credit.name}
                                    </a>
                                ) : (
                                    credit.name
                                )} - {credits_lang?.extra_credits?.credits[index]?.credit ?? credit.credit}
                                {credit.extra?.map((extra: string) => (
                                    <span key={extra}> {extra}</span>
                                ))}
                            </div>
                        );
                    })}
                </div>
            </div>

            <div className="info-banner" style={{ marginTop: "16px" }}>
                🌐 <a href={credits.development_server.url} target="_blank" rel="noreferrer">{credits_lang?.development_server?.label ?? credits.development_server.label}</a> {credits_lang?.development_server?.message ??credits.development_server.message}
            </div>
        </>
    );
}
