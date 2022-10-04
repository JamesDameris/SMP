# Profile 

## Process
1. Get Steam ID for user3
2. Create Player struct for Steam ID
3. Use Steam ID to get user profile information:

```
https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0002.29

GetPlayerSummaries (v0002)
Example URL: http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=XXXXXXXXXXXXXXXXXXXXXXX&steamids=76561197960435530 (This will show Robin Walker's profile information.)

Returns basic profile information for a list of 64-bit Steam IDs.

Arguments
    steamids
        Comma-delimited list of 64 bit Steam IDs to return profile information for. Up to 100 Steam IDs can be requested.
    format
        Output format. json (default), xml or vdf.

Return Value
    Some data associated with a Steam account may be hidden if the user has their profile visibility set to "Friends Only" or "Private". In that case, only public data will be returned.

Public Data
    steamid
        64bit SteamID of the user
    personaname
        The player's persona name (display name)
    profileurl
        The full URL of the player's Steam Community profile.
    avatar
        The full URL of the player's 32x32px avatar. If the user hasn't configured an avatar, this will be the default ? avatar.
    avatarmedium
        The full URL of the player's 64x64px avatar. If the user hasn't configured an avatar, this will be the default ? avatar.
    avatarfull
        The full URL of the player's 184x184px avatar. If the user hasn't configured an avatar, this will be the default ? avatar.
    personastate
        The user's current status. 0 - Offline, 1 - Online, 2 - Busy, 3 - Away, 4 - Snooze, 5 - looking to trade, 6 - looking to play. If the player's profile is private, this will always be "0", except is the user has set their status to looking to trade or looking to play, because a bug makes those status appear even if the profile is private.
    communityvisibilitystate
        This represents whether the profile is visible or not, and if it is visible, why you are allowed to see it. Note that because this WebAPI does not use authentication, there are only two possible values returned: 1 - the profile is not visible to you (Private, Friends Only, etc), 3 - the profile is "Public", and the data is visible. Mike Blaszczak's post on Steam forums says, "The community visibility state this API returns is different than the privacy state. It's the effective visibility state from the account making the request to the account being viewed given the requesting account's relationship to the viewed account."
    profilestate
        If set, indicates the user has a community profile configured (will be set to '1')
    lastlogoff
        The last time the user was online, in unix time.
    commentpermission
        If set, indicates the profile allows public comments.
```
4. Add relevant profile information to the player struct
5. Get Item IDs Using the Steam ID `https://api.steampowered.com/IEconItems_730/GetPlayerItems/v1/`
6. Add items to player struct
    - On add, fetch price info using the steam-marketplace-api and update player struct's total value