#TODO: Add json api calls here including compressed file download from github when file is missing
#           web JSON API CALL example localhost:5555/api/json?file_shorthand
#                              |   or localhost:5555/api/pjson?url_friendly_file_path
#                              v
#                          can be FOUND?
#                              |
#                              |-------- YES ------|
#                              v                   |
#                             NO                   |
#                              |                   |
#                              v                   |
#              request compressed file from github
# "/external_assets/compressed/API/JSON/lang/{lang_code}.gz.b64"
#                              |                   |
#                              v                   |
#                        base64 decode             |
#                              |                   |
#                              v                   |
#                       gzip decompress            |
#                              |                   |
#                              v                   |
#                          save file               |
#                              |                   |
#                              v                   |
#                     send file to client <--------|



#TODO: Move all text into this script for future translations help
#      language code tag used https://docs.sqanit.com/glossary/language-tags/
#      instead of "-" use "_" for better file name scheme
#           web LANG API CALL example localhost:5555/api/lang?lang_code
#                              |
#                              v
#                          can be FOUND?
#                              |
#                              |-------- YES ------|
#                              v                   |
#                             NO                   |
#                              |                   |
#                              v                   |
#              request compressed file from github
# "/external_assets/compressed/API/JSON/lang/{lang_code}.gz.b64"
#                              |                   |
#                              v                   |
#                        base64 decode             |
#                              |                   |
#                              v                   |
#                       gzip decompress            |
#                              |                   |
#                              v                   |
#                          save file               |
#                              |                   |
#                              v                   |
#                     send file to client <--------|
#
#NOTE: we might have to store the encoding somewhere incase we translate for a language not covered by utf-8
#  lang example for en_us.json
#  {
#     "credits": {
#         "originalCreators": "Original Creators",
#         "extra": "Extra Credits",
#         "support": "Support Us",
#         "donators": "Donators Hall of Fame"
#     }
#  }




#NOTE: Why download "FILE.json.gz.b64" instead of just "FILE.json"?
#       To put simply file size, whilst also still being possible for the user
#       to just take the text and decode+decompress it themselves if they don't
#       trust it directly.
#       for example:
#          you can decode "external_assets\compressed\API\JSON\credits.json.gz.b64"
#          on "https://tools.simonwillison.net/base64-gzip-decoder" and it will return
#          a json minified version of "external_assets\source\API\JSON\credits.json"
#       but do note that being a base64 encode of the normal file means
#       we lose some end file size efficiency, for example the above credits.json
#       source file is 4,883 Bytes, where as the gzip compressed file is 1,065 Bytes
#       but we sacrifice a little bit of file size for ease-of-use enduser decoding
#       that little bit of comfort costs some bytes but typically not as much
#       end file size is 1,420 Bytes ~70.9% reduction in filesize,a loss of
#       ~7.29% over just binary compression
#
#       !@! these are just values based on one file !@!
#       !@! compression effiency can be different depending on the source!@!

#NOTE: Why not store the compressed json instead of the raw one?
#       more or less same reason as above, enduser comfort. We can't hide anything
#       if its completely readable! But also it loads faster if we don't have to
#       decode and decompress at runtime each load