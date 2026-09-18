import { useState, useEffect } from "react";
import "../App.css";
import { Translate } from "../utils/ExtendedPageData";

interface RecorderWindowProps {
    initialMode?: "obby" | "potion";
    onClose?: () => void;
}

export default function RecorderWindow({ initialMode, onClose }: RecorderWindowProps = {}) {
    const [recording, setRecording] = useState(false);
    const [elapsed, setElapsed] = useState(0);
    const [statusMsg, setStatusMsg] = useState("Ready");

    // Mode: "obby" (default) or "potion"
    const [mode, setMode] = useState<"obby" | "potion">(initialMode || "obby");
    const [potionName, setPotionName] = useState("");

    // Track active replay state to ignore clicks (only for Obby currently)
    const [isReplaying, setIsReplaying] = useState(false);

    const [replayCountdown, setReplayCountdown] = useState<number | null>(null);
    const [pendingAction, setPendingAction] = useState<"replay" | "align" | null>(null);

    useEffect(() => {
        // Only check URL params when not rendered inline with props
        if (initialMode) {
            if (initialMode === "potion") setStatusMsg(Translate("recorder.potion_mode_ready"));
            return;
        }
        const params = new URLSearchParams(window.location.search);
        const modeParam = params.get("mode");
        if (modeParam === "potion") {
            setMode("potion");
            setStatusMsg(Translate("recorder.potion_mode_ready"));
        }
    }, []);

    useEffect(() => {
        let interval: any;
        if (recording) {
            interval = setInterval(() => {
                setElapsed(e => e + 1);
            }, 1000);
        } else {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [recording]);

    // Countdown Effect
    useEffect(() => {
        let interval: any;
        if (replayCountdown !== null && replayCountdown > 0) {
            interval = setInterval(() => {
                setReplayCountdown(prev => (prev !== null ? prev - 1 : null));
            }, 1000);
        } else if (replayCountdown === 0) {
            // Trigger Pending Action
            setReplayCountdown(null);

            if (pendingAction === "replay") {
                handleReplayAction();
            } else if (pendingAction === "align") {
                handleAlignAction();
            }
            setPendingAction(null);
        }
        return () => clearInterval(interval);
    }, [replayCountdown, pendingAction]);

    const formatTime = (sec: number) => {
        const m = Math.floor(sec / 60).toString().padStart(2, "0");
        const s = (sec % 60).toString().padStart(2, "0");
        return `${m}:${s} `;
    };

    const handleStart = async () => {
        if (replayCountdown !== null || isReplaying) return; // Disable if replaying

        if (mode === "potion" && !potionName.trim()) {
            setStatusMsg(Translate("common.error",[{from:"error",to:Translate("recorder.enter_a_name_first")}]));
            return;
        }

        try {
            if (window.pywebview && window.pywebview.api) {
                await window.pywebview.api.start_macro_recording();
                setRecording(true);
                setElapsed(0);
                setStatusMsg(Translate("recorder.recording"));
            } else {
                setStatusMsg(Translate("common.error",[{from:"error",to:"pywebview API not available"}]));
            }
        } catch (e) {
            setStatusMsg(Translate("common.error",[{from:"error",to:String(e)}]));
        }
    };

    const handleStop = async () => {
        if (isReplaying) return; // Safety guard
        try {
            if (window.pywebview && window.pywebview.api) {
                if (mode === "potion") {
                    await window.pywebview.api.stop_macro_recording_potion(potionName);
                    setRecording(false);
                    setStatusMsg(Translate("recorder.saved_to_value_json", [{ from: "value", to: potionName }]));
                } else {
                    await window.pywebview.api.stop_macro_recording();
                    setRecording(false);
                    setStatusMsg(Translate("recorder.saved"));
                }
            } else {
                setStatusMsg(Translate("common.error",[{from:"error",to:"pywebview API not available"}]));
            }
        } catch (e) {
            setStatusMsg(Translate("common.error",[{from:"error",to:String(e)}]));
        }
    };

    const handleReplayClick = () => {
        if (recording || isReplaying) return;
        setPendingAction("replay");
        setReplayCountdown(5);
        setStatusMsg(Translate("recorder.replaying_in_5s"));
    };

    const handleAlignClick = () => {
        if (recording || isReplaying) return;
        setPendingAction("align");
        setReplayCountdown(5);
        setStatusMsg(Translate("recorder.aligning_in_5s"));
    };

    const handleReplayAction = async () => {
        setStatusMsg(Translate("recorder.replaying"));
        setIsReplaying(true);
        try {
            if (window.pywebview && window.pywebview.api) {
                let result: string;
                if (mode === "potion") {
                    result = await window.pywebview.api.replay_potion_recording(potionName);
                } else {
                    result = await window.pywebview.api.replay_recording();
                }
                if (result && result.startsWith("Error:")) {
                    setStatusMsg(result);
                } else {
                    setStatusMsg(result === "Cancelled" ? Translate("recorder.replay_cancelled") : Translate("recorder.replay_finished"));
                }
            }
        } catch (e) {
            setStatusMsg(Translate("common.error",[{from:"error",to:String(e)}]));
        } finally {
            setIsReplaying(false);
        }
    };

    const handleAlignAction = async () => {
        setStatusMsg(Translate("recorder.aligning"));
        setIsReplaying(true); // Lock UI
        try {
            if (window.pywebview && window.pywebview.api) {
                await window.pywebview.api.align_camera();
            }
            setStatusMsg(Translate("recorder.aligned"));
        } catch (e) {
            setStatusMsg(Translate("common.error",[{from:"error",to:String(e)}]));
        } finally {
            setIsReplaying(false);
        }
    };

    return (
        <div style={{
            height: "100vh",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            background: "var(--bg-dark)",
            color: "var(--text-primary)",
            padding: "20px",
            border: "1px solid var(--border-color)",
            position: "relative"
        }}>
            {/* Corner Brackets for consistency */}
            <div className="corner-bracket tl" style={{ top: 5, left: 5 }} />
            <div className="corner-bracket tr" style={{ top: 5, right: 5 }} />
            <div className="corner-bracket bl" style={{ bottom: 5, left: 5 }} />
            <div className="corner-bracket br" style={{ bottom: 5, right: 5 }} />

            {onClose && (
                <button
                    onClick={onClose}
                    style={{
                        position: "absolute", top: 8, right: 12,
                        background: "none", border: "none", color: "var(--text-secondary)",
                        fontSize: "18px", cursor: "pointer", padding: "4px 8px",
                        lineHeight: 1
                    }}
                    title={Translate("common.close")}
                >
                    ✕
                </button>
            )}

            <h3 style={{ margin: "0 0 10px 0", color: "var(--accent)" }}>
                {mode === "potion" ? "Potion Recorder" : "Obby Recorder"}
            </h3>

            <div style={{ fontSize: "24px", fontFamily: "monospace", marginBottom: "15px" }}>
                {replayCountdown !== null ? Translate("recorder.starting_in_x", [{ from: "value", to: replayCountdown }]) : formatTime(elapsed)}
            </div>

            <div style={{ marginBottom: "10px", fontSize: "12px", color: recording || isReplaying ? "var(--accent)" : "var(--text-secondary)" }}>
                {statusMsg}
            </div>

            {mode === "potion" && !recording && (
                <div style={{ marginBottom: "10px", width: "100%" }}>
                    <input
                        type="text"
                        placeholder={Translate("recorder.placeholder_potion_name")}
                        value={potionName}
                        onChange={(e) => setPotionName(e.target.value)}
                        className="form-input"
                        style={{ width: "100%", textAlign: "center" }}
                    />
                </div>
            )}

            <div style={{ display: "flex", gap: "10px" }}>
                {!recording ? (
                    <>
                        <button
                            className="btn btn-start"
                            onClick={handleStart}
                            disabled={replayCountdown !== null || isReplaying}
                            style={{ padding: "8px 20px", opacity: (replayCountdown !== null || isReplaying) ? 0.5 : 1 }}
                        >
                            {Translate("common.start")}
                        </button>

                        <button
                            className="btn"
                            onClick={handleReplayClick}
                            disabled={replayCountdown !== null || isReplaying || (mode === "potion" && !potionName)}
                            style={{ padding: "8px 20px", backgroundColor: "#2196F3", color: "white", opacity: (replayCountdown !== null || isReplaying || (mode === "potion" && !potionName)) ? 0.5 : 1 }}
                        >
                            {mode === "potion" ? Translate("recorder.replay_save") : Translate("recorder.replay")}
                        </button>

                        {mode === "obby" && (
                            <button
                                className="btn"
                                onClick={handleAlignClick}
                                disabled={replayCountdown !== null || isReplaying}
                                style={{ padding: "8px 20px", backgroundColor: "#9C27B0", color: "white", opacity: (replayCountdown !== null || isReplaying) ? 0.5 : 1 }}
                            >
                                {Translate("recorder.align_camera")}
                            </button>
                        )}
                    </>
                ) : (
                    <button className="btn btn-stop" onClick={handleStop} style={{ padding: "8px 20px" }}>
                        {Translate("common.stop")}{" & "}{Translate("common.save")}
                    </button>
                )}
            </div>

            <div style={{ marginTop: "10px", fontSize: "10px", color: "gray" }}>
                {mode === "potion" ? Translate("recorder.make_sure_to_save") : Translate("recorder.obby_recorder")}
            </div>
        </div>
    );
}
