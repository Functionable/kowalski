print(package.path)
local jsonLib = require "json.lua"

local config = jsonLib.decode(File.load("config.json"))

local enums = {
	["BLF"] = {
		"BLF_NULL", 
		"BLF_INT", 
		"BLF_FLOAT", 
		"BLF_BOOL", 
		"BLF_DOUBLE", 
		"BLF_STRING", 
		"BLF_OBJECTREFERENCE",
		"BLF_LONG"
	}
}

local function shallowcopy(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in pairs(orig) do
            copy[orig_key] = orig_value
        end
    else -- number, string, boolean, etc
        copy = orig
    end
    return copy
end

local globalCopy = shallowcopy(_G)

print(jsonLib.encode(enums))

local typeF = type
local pairsF = pairs
local fileWrite = File.save
local closeGame = os.close

local function printTable(value)
	for k, v in pairs(value) do
		if( type(v) == "table") then
			print(k)
			printTable(v)
		else
			print(k..": "..tostring(v))
		end
	end
end

local function processTable(table) 
	for key, value in pairs(table) do
		if type(value) == "function" then
			table[key] = "function"
		elseif type(value) == "string" then
			table[key] = value
		elseif type(value) == "number" or type(value) == "integer" then
			table[key] = tostring(value)
		end
		if( type(value) == "table") then
			processTable(value)
		end
	end
end

globalCopy._G = nil
globalCopy.package = nil
globalCopy.string = shallowcopy(string)
globalCopy.table = shallowcopy(table)
globalCopy.math = shallowcopy(math)
--globalCopy.math.huge = "number"

local metatableList = {}
if( listblurmetatables ~= nil) then
	for k, v in pairs(listblurmetatables()) do
		metatableList[k] = v
	end
else
	for k, v in pairs(config.classes) do
		metatableList[v] = findmetatable(v)
	end
end

processTable(metatableList)

local reportDetails = {
	["globals"] = globalCopy,
	["classes"] = metatableList 
}

processTable(globalCopy)
fileWrite("report.json", jsonLib.encode(reportDetails))

closeGame(0)
