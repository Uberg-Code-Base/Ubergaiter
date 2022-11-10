import './style.css';
import {Map, View} from 'ol';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer';
import {OSM, Vector as VectorSource} from 'ol/source';
import GeoJSON from 'ol/format/GeoJSON';
import {transform} from 'ol/proj.js';
import {useGeographic} from 'ol/proj';
import {Circle, Point} from 'ol/geom';
import {toStringXY} from 'ol/coordinate';
import {MultiPoint} from 'ol/geom';
import {fromLonLat} from 'ol/proj';

import {
  Circle as CircleStyle,
  Fill,
  Stroke,
  Style,
  Text,
} from 'ol/style';
import LineString from 'ol/geom/LineString';


//useGeographic();



//top-left reference point
var p0 = {
    lng: 45.363627,    // Latitude
    lat: -72.234315,    // Longitude
    x: 0,
    y: 0
}
var p1 = fromLonLat([p0.lat,p0.lng])
p0.x = p1[0]
p0.y = p1[1]

console.log(p0.x)

const coord = [p0.lat,p0.lng];
const place = toStringXY(coord, 8);

console.log(place)
//p0.pos = latlngToGlobalXY(p0.lat, p0.lng);


const point = new Point(place);
// Lines
function lineStyleFunction(feature, resolution) {
  return new Style({
    stroke: new Stroke({
      color: 'green',
      width:1,    }),
  });
}


/////////
const sandStroke = new Stroke({
  color:'orange',
  width:1,
})
const sandFill = new Fill({
  color: 'orange'
})
function SandStyleFunction(feature, resolution) {
  return new Style({
    image: new CircleStyle({
      fill:sandFill,
      stroke:sandStroke,
      radius:3
    }),
    fill:sandFill,
    stroke:sandStroke
    });
}
const SandLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/SandPath.geojson',
    format: new GeoJSON(),
  }),
  style: SandStyleFunction,
});

///////////////
/////////
const nothingStroke = new Stroke({
  color:'black',
  width:1,
})
const nothingFill = new Fill({
  color: 'black'
})
function NothingStyleFunction(feature, resolution) {
  return new Style({
    image: new CircleStyle({
      fill:nothingFill,
      stroke:nothingStroke,
      radius:3
    }),
    fill:nothingFill,
    stroke:nothingStroke
    });
}
const NothingLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/NothingPath.geojson',
    format: new GeoJSON(),
  }),
  style: NothingStyleFunction,
});

///////////////
/////////
const remStroke = new Stroke({
  color:'blue',
  width:1,
})
const remFill = new Fill({
  color: 'blue'
})
function RemStyleFunction(feature, resolution) {
  return new Style({
    image: new CircleStyle({
      fill:remFill,
      stroke:remStroke,
      radius:3
    }),
    fill:remFill,
    stroke:remStroke
    });
}
const RemLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/RemPath.geojson',
    format: new GeoJSON(),
  }),
  style: RemStyleFunction,
});

///////////////
/////////
const myrioStroke = new Stroke({
  color:'white',
  width:1,
})
const myrioFill = new Fill({
  color: 'white'
})
function MyrioStyleFunction(feature, resolution) {
  return new Style({
    image: new CircleStyle({
      fill:myrioFill,
      stroke:myrioStroke,
      radius:3
    }),
    fill:myrioFill,
    stroke:myrioStroke
    });
}
const MyrioLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/MyrioPath.geojson',
    format: new GeoJSON(),
  }),
  style: MyrioStyleFunction,
});

///////////////
/////////
const eloStroke = new Stroke({
  color:'purple',
  width:1,
})
const eloFill = new Fill({
  color: 'purple'
})
function EloStyleFunction(feature, resolution) {
  return new Style({
    image: new CircleStyle({
      fill:eloFill,
      stroke:eloStroke,
      radius:3
    }),
    fill:eloFill,
    stroke:eloStroke
    });
}
const EloLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/ElodaePath.geojson',
    format: new GeoJSON(),
  }),
  style: EloStyleFunction,
});

///////////////
/////////
const utriStroke = new Stroke({
  color:'green',
  width:1,
})
const utriFill = new Fill({
  color: 'green'
})
function UtriStyleFunction(feature, resolution) {
  return new Style({
    image: new CircleStyle({
      fill:utriFill,
      stroke:utriStroke,
      radius:3
    }),
    fill:utriFill,
    stroke:utriStroke
    });
}
const UtriLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/UtriPath.geojson',
    format: new GeoJSON(),
  }),
  style: UtriStyleFunction,
});

///////////////
  const ampStroke = new Stroke({
    color:'red',
    width:1,
  })
  const ampFill = new Fill({
    color: 'red'
  })
  function AmpStyleFunction(feature, resolution) {
    return new Style({
      image: new CircleStyle({
        fill:ampFill,
        stroke:ampStroke,
        radius:3
      }),
      fill:ampFill,
      stroke:ampStroke
      });
    }  



const AmpLines = new VectorLayer({
  source: new VectorSource({
    url: 'data/geojson/AmpliPath.geojson',
    format: new GeoJSON(),
  }),
  style: AmpStyleFunction,
});



const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM()
    }),
    UtriLines,
    AmpLines,
    NothingLines,
    SandLines,
    EloLines,
    RemLines,
    MyrioLines
  ],
  view: new View({
    //center: new OpenLayers.LonLat(p0.lat,p0.lng).transform(new OpenLayers.Projection('EPSG:4326'), new OpenLayers.Projection('EPSG:3857')),
    //center: fromLonLat([p0.lat, p0.lng]) ,
    //projection: 'EPSG:3857',
    center: [p0.x, p0.y],
    zoom: 17,
  })
  
});
UtriLines.getSource().on('change', function(evt){
  var source = evt.target;
  console.log(source)
  if (source.getState() === 'ready') {
    var numFeatures = source.getFeatures().length; 
    console.log("Count after change: " + numFeatures);
  }
});
AmpLines.getSource().on('change', function(evt){
  var source = evt.target;
  console.log(source)
  if (source.getState() === 'ready') {
    var numFeatures = source.getFeatures().length; 
    console.log("Count after change: " + numFeatures);
  }
});

