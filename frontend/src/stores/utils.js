import { draw, parse as jsrootParse } from 'jsroot';

export async function drawHistJson(histJson, domId) {
    const obj = await jsrootParse(JSON.stringify(histJson));
    console.log('Read object of type', obj._typename, domId);
    return draw(domId, obj, "hist");
}      
