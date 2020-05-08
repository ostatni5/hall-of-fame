function arrayRotate(arr, reverse) {
    if (reverse) arr.unshift(arr.pop());
    else arr.push(arr.shift());
    return arr;
}

function getPrettyDate(date){
    const mo = new Intl.DateTimeFormat('en', { month: 'short' }).format(date)
    const da = new Intl.DateTimeFormat('en', { day: '2-digit' }).format(date)
    return `${da}-${mo}`
}


function getEvenlySpacedColors(myData){
    let colors = []
    let length = Math.max.apply(null, myData) - Math.min.apply(null, myData) + 1
    // 270 because we don't want the spectrum to circle back
    let step = 270/length;
    for (let i = 1; i <= length; i++) {
        let color = hslToRgb((i)*step, 0.5, 0.5);
        colors.push(color);
    }
    return colors
}