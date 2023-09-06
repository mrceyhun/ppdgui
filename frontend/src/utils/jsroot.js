import { draw, parse as jsrootParse } from 'jsroot';

export async function drawHistJson(domId, histJson) {
    const obj = await jsrootParse(histJson);
    // console.log('Read object of type', obj._typename, domId);
    return draw(domId, obj, "hist");
}      
