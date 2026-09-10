
/*
 * @DEV-ONLY
 * @REPLACE 'import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"' WITH ''
 * @REPLACE 'import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"' WITH ''
 * @REPLACE 'typeof json_credits_data' WITH 'any'
 * @REPLACE 'typeof json_lang_data' WITH 'any'
 */
import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"
import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"

export interface ExtendedProperties {
    creditsData: typeof json_credits_data | null;
    langData:    typeof json_lang_data | null;
}

export class PageIcons {
    public static Auras         :string = "✨"
    public static Record        :string = "🎬"
    public static Autopop       :string = "🧪"
}