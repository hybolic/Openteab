import { Translate } from "../utils/ExtendedPageData";

const WEBHOOK_PATTERNS = [
    /discord\.com\/api\/webhooks/i,
    /discordapp\.com\/api\/webhooks/i,
    /discord\.com\/api\//i,
];

export function looksLikeWebhookUrl(value: string): boolean {
    if (!value || value.trim().length === 0) return false;
    return WEBHOOK_PATTERNS.some((pattern) => pattern.test(value));
}

export function getWebhookWarning(value: string, fieldName: string): string | null {
    if (!looksLikeWebhookUrl(value)) return null;
    return Translate("webhook.webhook_warn", [{ from: "fieldName", to: fieldName }]);
}