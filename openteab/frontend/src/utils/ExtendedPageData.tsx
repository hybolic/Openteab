import type React from "react"
/*
 * @DEV-ONLY
 * @REPLACE 'import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"' WITH ''
 * @REPLACE 'import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"' WITH ''
 * @REPLACE 'typeof json_credits_data' WITH 'any'
 * @REPLACE 'typeof json_lang_data' WITH 'any'
 * @REPLACE 'import openteab_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/openteab.json"' WITH 'import openteab from "./json/openteab.json"'
 * @REPLACE 'import roblox_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/roblox.json"' WITH 'import roblox from "./json/roblox.json"'
 * @REPLACE 'import EmoteList_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/emotes.json"' WITH 'import EmoteList_json from "./json/emotes.json"'
 * @REPLACE 'export let EmoteList = EmoteList_json' WITH 'export let EmoteList : Record<string,Emote> = EmoteList_json'

 */
import json_lang_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/lang/en_us.json"
import json_credits_data from "D:/Github/Noteab-Macro/external_assets/source/API/JSON/credits.json"
import EmoteList_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/emotes.json"
import openteab_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/openteab.json"
import roblox_json from "D:/Github/Noteab-Macro/openteab/frontend/public/json/roblox.json"


export const langData = json_lang_data //used as reference when replacing, do not use in production
export const openteab = openteab_json
export const roblox = roblox_json
export type LangData = typeof json_lang_data
export type LangConst = {JSON?:LangData,FLATPACK:Map<string,string>}
export type CreditsData = typeof json_credits_data

//storage of langs
export let LANGS:Map<string,LangConst> = new Map<string,LangConst>()
export let CURRENT_LANG:string="en_us"

//storage of credits
export let CREDITS:CreditsData

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
        const file:string = url_data.concat(".gz.b64")
        if (this.isLoaded())
            return true
        console.log("[LangLoader] Sending JSON API FETCH to BACKEND")
        try{
            const response = await fetch("/api/lang?"+url_data)
            if (response.ok){
                console.log("Lang Data received Locally!")
                this.setData(await response.json())
                this.isLoaded(true)
            }
        }catch(e){
            console.log("Local Lang file failed:", e)
        }
        if (!this.isLoaded()) {
            try{
                const response = await fetch(file)
                if (response.ok){
                    console.log("Lang Data received from Github!")
                    this.setData(await LOAD_JSON.decodeBackup(await response.json()))
                    this.isLoaded(true)
                }
            }catch(error){
                console.log("FAILED TO GET " + file + " from github!", error)
            }
        }
        this.FLATPACK = this.flattenTranslations(this.getData(), "", this.FLATPACK)
        this.setData(null)
        return true
    }

    flattenTranslations(data: unknown, prefix = "", result = new Map<string, string>()): Map<string, string> {
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

export class EmoteLoader extends LOAD_JSON {
    static instance = new EmoteLoader()
    static EmoteList = EmoteList_json
    async LOAD() : Promise<boolean>
    {
        if (this.isLoaded())
            return this.isLoaded()
        console.log("LOADING EMOTES")
        for (const emote of Object.values(EmoteLoader.EmoteList))
        {
            // console.log("LOADING EMOTE:",emote.emote)
            if (Object.hasOwn(emote, "klipy"))
            {
                console.log("EMOTE CONTAINS KLIPY:",emote.emote)
                emote.url = await this.resolveKlipyEmote(emote)
            }
        }
        return this.isLoaded(true)
    }

    async resolveKlipyEmote(emote:Emote):Promise<string>{
        if (!emote.klipy) return emote.url
        
        let response = await fetch("/api/emote?file="+emote.klipy.slug+"&nofile=1")
        if (response.ok)
        {
            console.log("Emote:","localally sourced")
            return "/api/emote?file="+emote.klipy.slug
        }
        if (emote.klipy.file_type)
        {
            console.log("Emote:","get online")
            return this.resolveKlipySlug(emote.klipy.slug, emote.klipy.fallback, emote.klipy.file_type)
        }
        return this.resolveKlipySlug(emote.klipy.slug, emote.klipy.fallback)
    }

    async resolveKlipySlug(slug:string, fallback:string, file_type:string="WEBP"):Promise<string>
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
                        return file
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

    static getEmote(emote:string):Emote|undefined{
        return Object.values(this.EmoteList).find(x => x.emote === emote)
    }
}

interface Emote
{
    emote:string
    url:string
    klipy?:{
        slug:string
        fallback:string
        file_type?:string
    }
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

interface KLIPY_API {
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


const INLINES = [
    {inline:"WARN",regex:/\[WARN\]\{(.*?)\}/,func:(result: RegExpMatchArray)=><b style={{ color: "#ff6b6b" }}>{result[1]}</b>},
    {inline:"BR",regex:/\[BR\]/,func:()=><br/>},
    {inline:"ITALIC",regex:/\[ITALIC\]\{(.*?)\}/,func:(result: RegExpMatchArray)=><i>{result[1]}</i>},
    {inline:"LINK",regex:/\[LINK=(.*?)\]\{(.*?)\}/,func:(result: RegExpMatchArray)=>{
        //i don't think i could optimise this if i tried lmao
        const value = result[1].split(".").reduce((obj: any, key) => obj?.[key], { openteab, roblox })
        const url = typeof value === "string" ? value : "#"
        return (<a href={url} target="_blank" rel="noreferrer">{result[1] === result[2] ? url : result[2]}</a>)}
    }
]
const EMOTE_REGEX:RegExp=/:[a-zA-Z\-_0-9]+:/
let REGEX_ALL:RegExp
let PRECHECK_REGEX_ALL:RegExp
export async function LOAD_ALL(): Promise<void>
{

    //regex compile for inline checks
    REGEX_ALL = new RegExp(`(${INLINES.map(x => x.regex.source).join("|")}|${EMOTE_REGEX.source})`,"g")
    PRECHECK_REGEX_ALL = new RegExp(`(${INLINES.map(x => `\\[${x.inline}(?:=[^\\]]+)?\\]`).join("|")}|${EMOTE_REGEX.source})`)

    await CreditsLoader.instance.LOAD()
    CREDITS = CreditsLoader.instance.getData() as CreditsData

    //load fallback lang first "en_us"
    await LangLoader.instance.LOAD("en_us")
    LANGS.set("en_us",{FLATPACK: LangLoader.instance.FLATPACK})

    //resolve the emotes list, if something is missing we just redirect where appropriate
    EmoteLoader.instance.LOAD()
    console.log("DONE EMOTES!!")
}


export class PageIcons {
    public static Auras         :string = "✨"
    public static Record        :string = "🎬"
    public static Autopop       :string = "🧪"
    public static SupportUs     :string = "💎"
    public static Donator       :string = "🏆"
    public static Fishing       :string = "🎣"
    public static Fishing_cal   :string = "📍"
    public static CalibrationMouse:string = "🧭"
    public static Credits       :string = "🌐"
    public static Ping          :string = "🔔"
    public static Merchant      :string = "🏪"
    public static Mari          :string = "🎒"
    public static Jester        :string = "🃏"
    public static JesterExchange:string = "💱"
    public static Rin           :string = "🦊"
    public static Misc_ItemUsage:string = "📦"
    public static Misc_Limbo    :string = "⚡"
    public static Misc_Quests   :string = "📸"
    public static Misc_BiomeRecording:string = "🎬"
    public static Movements :string="⚙️"
    public static Movements_obby :string="🗺️"


    public static UP   :string = "▲"
    public static DOWN :string = "▼"
}


export function Translate(key:string,replacement?:{from:string,to:any}[]|null, language?:string,stringify?:true): string
export function Translate(key:string,replacement?:{from:string,to:any}[]|null, language?:string,stringify?:false): React.ReactNode

export function Translate(key:string,replacement:{from:string,to:any}[]|null=null, language:string|null=null,stringify:boolean=false): string|React.ReactNode {
    //debug output translate contents
    // console.log(key,replacement,language,stringify)
    const LANG = LANGS.get((language ?? CURRENT_LANG).toLowerCase()) ?? LANGS.get("en_us")

    if (!LANG?.FLATPACK)
    {
        console.log("LANG.FLATPACK missing!", key)
        return null
    }

    let result = LANG.FLATPACK.get(key)

    if (typeof result !== "string")
    {
        console.log("key not string,", key, "result", result)
        return null
    }

    replacement?.forEach(({from,to})=>result=result?.replaceAll(`{${from}}`,String(to)))

    return !stringify && PRECHECK_REGEX_ALL.test(result) ? replaceInlines(result) : String(result)
}

export function replaceInlines(text: string): React.ReactNode {
    const result: React.ReactNode[] = []
    let last_index = 0

    for (const match of text.matchAll(REGEX_ALL))
    {
        const match_index = match.index!
        if (match_index > last_index)
            result.push(text.slice(last_index,match_index))

        const match_value = match[0]
        const inline = INLINES.find(x => x.regex.test(match_value))

        if(inline)
            result.push(inline.func(match_value.match(inline.regex)!))
        else if (EMOTE_REGEX.test(match_value))
        {
            const emote = EmoteLoader.getEmote(match_value)

            if (emote)
                result.push(<img src={emote.url} alt={emote.emote} style={{ width: "auto", height: "15px", position: "relative", top: "4px", }}/>)
            else
                result.push(match_value)
        }
        last_index = match_index + match_value.length
    }

    if (last_index < text.length)
        result.push(text.slice(last_index))
    
    return result;
}