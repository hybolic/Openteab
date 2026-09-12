
/*
 * @DEV-ONLY
 * @REPLACE 'import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"' WITH ''
 * @REPLACE 'import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"' WITH ''
 * @REPLACE 'typeof json_credits_data' WITH 'any'
 * @REPLACE 'typeof json_lang_data' WITH 'any'
 */
import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"
import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"

export type LangData    = typeof json_lang_data
export type CreditsData = typeof json_credits_data

export interface ExtendedProperties {
    creditsData?: CreditsData;
    langData?:    LangData;
}

export class PageIcons {
    public static Auras         :string = "✨"
    public static Record        :string = "🎬"
    public static Autopop       :string = "🧪"
    public static SupportUs     :string = "💎"
    public static Donator       :string = "🏆"
    public static Fishing       :string = "🎣"
    public static Fishing_cal   :string = "📍"
}
export interface Emote
{
    emote:string
    url:string
    klipy?:{
        slug:string
        fallback:string
        file_type?:"GIF"|"PNG"|"WEBP"|"JPG"
    }
}
export let EmoteList = [
    {
        emote:":umamusume_mambo_dancing:",
        url:"/api/emote?file=mambo-dancing",
        klipy:{slug:"mambo-dancing",fallback:"https://static2.klipy.com/ii/2fd1ee858360694ebc7272832a866c2b/0d/9e/XNlKvEr2fq3CD2M.gif"}
    }
]
export async function LoadEmotes()
{
    if (LOADED)
        return LOADED
    console.log("LOADING EMOTES")
    for (const emote of EmoteList)
    {
        console.log("LOADING EMOTE",emote.emote)
        if (emote.klipy)
        {
            console.log(emote.emote, "EMOTE CONTAINS KLIPY")
            emote.url = await resolveKlipyEmote(emote)
        }
    }

    LOADED = true
    return LOADED
}

interface FILE_TYPE{
    url:string,
    width:number,
    height:number,
    size:number
}
interface FILE_TYPES {
    gif?:FILE_TYPE,
    png?:FILE_TYPE,
    webp?:FILE_TYPE,
    jpg?:FILE_TYPE
}
export interface KLIPY_API {
    result:boolean,
    data:
    {
        data:[
            {
                slug:string,
                file:{
                    hd?:FILE_TYPES,
                    md?:FILE_TYPES,
                    sm?:FILE_TYPES,
                    xs?:FILE_TYPES
                },
                type:string
            }
        ]
    }
}
let LOADED = false
export async function resolveKlipyEmote(emote:Emote):Promise<string>{
    if (!emote.klipy) return emote.url
    
    console.log("try get local")
    let response = await fetch("/api/emote?file="+emote.klipy.slug+"&nofile=1")
    if (response.ok)
        return "/api/emote?file="+emote.klipy.slug
    if (emote.klipy.file_type)
    {
        console.log("try get online")
        return resolveKlipySlug(emote.klipy.slug, emote.klipy.fallback, emote.klipy.file_type)
    }
    return resolveKlipySlug(emote.klipy.slug, emote.klipy.fallback)
}
export async function resolveKlipySlug(slug:string, fallback:string, file_type:"GIF"|"PNG"|"WEBP"|"JPG"="WEBP"):Promise<string>
{
    const url = "https://api.klipy.com/api/v1/web/gifs/items?slugs=" + slug
    const response = await fetch(url)
    if(!response.ok)
        return fallback
    const KLIPY_DATA:KLIPY_API = await response.json()
    if (!KLIPY_DATA.result)
        return fallback

    if (KLIPY_DATA.result){
        for (const KLIPY_ITEM of KLIPY_DATA.data.data) {
            if (KLIPY_ITEM.slug == slug)
            {
                const fileType = file_type.toLowerCase() as "gif" | "webp" | "jpg" | "png";
                const file = KLIPY_ITEM.file.xs?.[fileType]?.url ??
                    KLIPY_ITEM.file.sm?.[fileType]?.url ??
                    KLIPY_ITEM.file.md?.[fileType]?.url ??
                    KLIPY_ITEM.file.hd?.[fileType]?.url
                if (file && file != undefined)
                {
                    return file
                }
                if (fallback !== null && fallback !== "")
                    return fallback
                return (
                    KLIPY_ITEM.file.xs?.webp?.url ??
                    KLIPY_ITEM.file.sm?.webp?.url ??
                    KLIPY_ITEM.file.md?.webp?.url ??
                    KLIPY_ITEM.file.hd?.webp?.url ??
                    ""
                )
            }
        }
    }
    return fallback
}
export function replaceWithEmote(line: string) {
    if (!LOADED)
        return (<p style={{ lineHeight: "15px", margin: 0 }}>{line}</p>)
    try{
        let parts: React.ReactNode[] = [line]
        if (EmoteList == null)
            return
        EmoteList.forEach((element) => {
            const newResult: React.ReactNode[] = []

            parts.forEach((part) => {
                if (typeof part !== "string") {
                    newResult.push(part)
                    return
                }

                const split = part.split(element.emote)

                split.forEach((text, index) => {
                    newResult.push(text)
                    if (index < split.length - 1)
                        newResult.push( <img key={`${element.emote}-${newResult.length}`} src={element.url} alt={element.emote} style={{ width: "auto", height: "15px", position: "relative", top: "4px", }} /> )
                });
            });
            parts = newResult
        });

        return (<p style={{ lineHeight: "15px", margin: 0 }}>{parts}</p>)
    }catch{return(<p style={{ lineHeight: "15px", margin: 0 }}>{line}</p>)}
}