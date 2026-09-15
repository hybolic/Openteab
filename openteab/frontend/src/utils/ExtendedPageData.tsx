
/*
 * @DEV-ONLY
 * @REPLACE 'import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"' WITH ''
 * @REPLACE 'import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"' WITH ''
 * @REPLACE 'typeof json_credits_data' WITH 'any'
 * @REPLACE 'typeof json_lang_data' WITH 'any'
 * @REPLACE 'import openteab_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/openteab.json"' WITH 'import openteab from "./json/openteab.json"'
 * @REPLACE 'import roblox_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/roblox.json"' WITH 'import roblox from "./json/roblox.json"'
 * @REPLACE 'import EmoteList_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/emotes.json"' WITH 'import roblox from "./json/emotes.json"'
 * @REPLACE 'export let EmoteList = EmoteList_json' WITH 'export let EmoteList : Record<string,Emote> = EmoteList_json'

 */
import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"
import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"

export type LangData    = typeof json_lang_data
export type LangConst = {JSON:LangData,FLATPACK:Map<string,string>}
export type CreditsData = typeof json_credits_data

export interface ExtendedProperties {
    creditsData?: CreditsData
    langData?:    LangData
}
abstract class LOAD_JSON {
    private LOADED:boolean = false
    private DATA = {}
    private JSON_URL:string = "https://raw.githubusercontent.com/hybolic/Openteab/refs/heads/Openteab/external_assets/compressed/API/JSON/"
    abstract LOAD(url_data:string|undefined):Promise<boolean>
    getData() {return this.DATA}
    setData(data:any) {this.DATA = data; return this.DATA}
    isLoaded(done:boolean|undefined=undefined){
        if (done !== undefined)
            this.LOADED = done
        return this.LOADED
    }
    getJsonURL(file:string){return this.JSON_URL + file}
    static async decodeBackup(data: string): Promise<any> {
        const bin = Uint8Array.from(
            atob(data.trim()),
            (char) => char.charCodeAt(0)
        )

        const stream = new DecompressionStream("gzip")

        const decompressed = await new Response(new Blob([bin]).stream().pipeThrough(stream))
        .arrayBuffer()

        const json = new TextDecoder().decode(decompressed)

        return JSON.parse(json)
    }
}
export class CreditsLoader extends LOAD_JSON {
    static instance = new CreditsLoader()
    async LOAD(): Promise<boolean>
    {
        if (this.isLoaded())
            return this.isLoaded()
        console.log("[CreditsLoader] Sending JSON API FETCH to BACKEND")
        await fetch("/api/json?credits")
            .then((response) => response.json())
            .then((data) => {
                this.setData(data)
                console.log("Credits Data received!"/* , data */)
            })
            .catch((error) => {
                console.log("FAILED TO GET Credits.json locally, trying github!", error)
                fetch(this.getJsonURL("credits.gz.b64"))
                    .then((response) => response.text())
                    .then((data) => {
                        LOAD_JSON.decodeBackup(data).then((new_data) => {
                            this.setData(new_data)
                            console.log("Credits Data received from Github!"/* , new_data */)
                        })
                    }).catch((error) => {
                        console.log("FAILED TO GET Credits.json from github!", error)
                    })
            })
        return this.isLoaded(true)
    }
}

export class LangLoader extends LOAD_JSON {
    static instance = new LangLoader()
    FLATPACK:Map<string,string> = new Map<string, string>()
    async LOAD(url_data:string) : Promise<boolean>
    {
        if (this.isLoaded())
            return this.isLoaded()
        console.log("[LangLoader] Sending JSON API FETCH to BACKEND")
        await fetch("/api/lang?"+url_data)
            .then((response) => response.json())
            .then((data) => {
                this.setData(data)
                console.log("Credits Data received!"/* , data */)
            })
            .catch((error) => {
                console.log("FAILED TO GET "+url_data+".json locally, trying github!", error)
                let file:string = url_data.concat(".gz.b64")
                fetch(this.getJsonURL("LANG/" + file))
                    .then((response) => response.text())
                    .then((data) => {
                        LOAD_JSON.decodeBackup(data).then((new_data) => {
                            this.setData(new_data)
                            console.log("Lang Data received from Github!"/* , new_data */)
                        })
                    }).catch((error) => {
                        console.log("FAILED TO GET " + file + " from github!", error)
                    })
            }).finally(()=>{
        this.FLATPACK = this.flattenTranslations(this.getData(), "", this.FLATPACK)})
        return this.isLoaded(true)
    }

    flattenTranslations(data: unknown,prefix = "", result = new Map<string, string>()): Map<string, string> {
        if (typeof data !== "object" || data === null) return result

        for (const [key, value] of Object.entries(data)) {
            const fullKey = prefix ? `${prefix}.${key}` : key

            if (typeof value === "string")
                result.set(fullKey, value)
            else if (typeof value === "object" && value !== null)
                this.flattenTranslations(value, fullKey, result)
        }

        return result
    }
}

//storage of langs
export let LANGS:Map<string,LangConst> = new Map<string,LangConst>()
export let CURRENT_LANG:string="en_us"

//storage of credits
export let CREDITS:CreditsData

export function LOAD_ALL()
{
    CreditsLoader.instance.LOAD().then(()=>{
        CREDITS = CreditsLoader.instance.getData() as CreditsData
    })
    //load fallback lang first "en_us"
    LangLoader.instance.LOAD("en_us").then(()=>{
        LANGS.set("en_us",{JSON: LangLoader.instance.getData() as LangData, FLATPACK: LangLoader.instance.FLATPACK})
    })
    //resolve the emotes list, if something is missing we just redirect where appropriate
    LoadEmotes()
}


export class PageIcons {
    public static Auras         :string = "✨"
    public static Record        :string = "🎬"
    public static Autopop       :string = "🧪"
    public static SupportUs     :string = "💎"
    public static Donator       :string = "🏆"
    public static Fishing       :string = "🎣"
    public static Fishing_cal   :string = "📍"
    public static CalibrationMouse :string = "🧭"
    public static Credits       :string = "🌐"
    public static Ping          :string = "🔔"
    public static Merchant      :string = "🏪"
    public static Mari          :string = "🎒"
    public static Jester        :string = "🃏"
    public static JesterExchange:string = "💱"
    public static Rin           :string = "🦊"


    public static UP   :string = "▲"
    public static DOWN :string = "▼"
}


import openteab_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/openteab.json"
export const openteab = openteab_json

import roblox_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/roblox.json"
export const roblox = roblox_json

export function Translate(key:string,replacement:{from:string,to:string|number|boolean}[]|null=null, language:string|null=null): string {
    if (language === null)
        language = CURRENT_LANG
    let LANG = LANGS.get(language.toLowerCase())
    if (!LANG) { //do fallback
        LANG = LANGS.get("en_us")
        if (!LANG) {
            console.log("FALLBACK LANG MISSING!")
            return key
        }
    }
    const translation = LANG.FLATPACK
    if (!translation)
    {
        console.log("LANG.FLATPACK missing!")
        return key
    }
    
    let result = translation.get(key)

    if (typeof result !== "string")
    {
        console.log("key not string,", key, "result", result)
        return key
    }
    else if (replacement && replacement.length > 0) {
        let temp_var:string = result
        replacement.forEach(({from,to}) => {
            temp_var = temp_var.replaceAll(`{${from}}`, String(to))
        })
        result = temp_var
    }
    return result
}
export function replaceTranslateWithEmote(key:string,replacement:{from:string,to:string|number|boolean}[]|null=null, language:string|null=null) {
    return replaceWithEmote(Translate(key,replacement,language))
}

//EMOTE LOADER

import EmoteList_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/emotes.json"
export interface Emote
{
    emote:string
    url:string
    klipy?:{
        slug:string
        fallback:string
        file_type?:string
    }
}
export let EmoteList = EmoteList_json

export async function LoadEmotes()
{
    if (LOADED)
        return LOADED
    console.log("LOADING EMOTES")
    for (const emote of Object.values(EmoteList))
    {
        console.log("LOADING EMOTE",emote.emote)
        if (Object.hasOwn(emote, "klipy"))
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

export async function resolveKlipySlug(slug:string, fallback:string, file_type:string="WEBP"):Promise<string>
{
    if (!["GIF","PNG","WEBP","JPG"].includes(file_type))
        file_type = "WEBP"
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
                const fileType = file_type.toLowerCase() as "gif" | "webp" | "jpg" | "png"
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

let LOADED = false
export function replaceWithEmote(line: string) {
    if (!LOADED)
        return (<p style={{ lineHeight: "15px", margin: 0 }}>{line}</p>)
    try{
        let parts: React.ReactNode[] = [line]
        if (EmoteList == null)
            return
        Object.values(EmoteList).forEach((element) => {
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
                })
            })
            parts = newResult
        })

        return (<p style={{ lineHeight: "15px", margin: 0 }}>{parts}</p>)
    }catch{return(<p style={{ lineHeight: "15px", margin: 0 }}>{line}</p>)}
}