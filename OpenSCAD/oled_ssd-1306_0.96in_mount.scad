// Mount for a 128x64 0.96" SSD-1306 OLED module
// intended to mount above Pi Zero.
// Gregory A Sanders - Feb, 2025
//
// CENTER ALL CUBES
//
// fa = face
fax = 27;
fay = 27;
faz = 2;
// fo = face opening
fox = 24;
foy = 14;
foz = 8;
// fh = face hole spacing
fhx = 20;
fhy = 23;
fhz = 10;
// mh = Pi mount hole spacing
mhx = 58;
mhy = 23;


$fn=64;

module face(){
    difference(){
        cube([fax+2,fay+2,faz],true);
        translate([0,1,0])
        cube([fox,foy,foz],true);
    }
}
module side(){
    difference(){
        linear_extrude(2)
        hull(){
            square([29,8]);
            translate([(27/2),12,0])
            circle(8);
        }
        translate([27/2,14,-1])
        cylinder(20,2);
    }
}
module zeroscrew(){
    union(){
        cylinder(20,r=1.5);
        // cylinder(2.5,r=3);
    }
}
module oledscrew(){
    union(){
        cylinder(20,2);
        // cylinder(2,r=2);
    }
}
module zeroholes(){
    zeroscrew();
    translate([0,mhy,0])
    zeroscrew();
    translate([mhx,mhy,0])
    zeroscrew();
    translate([mhx,0,0])
    zeroscrew();
}
module oledholes(){
    oledscrew();
    translate([0,fhy,0])
    oledscrew();
    translate([fhx,fhy,0])
    oledscrew();
    translate([fhx,0,0])
    oledscrew();
}

module oledassy(){
    translate([-3-(fax/2),-1-fay/2,-1])
    rotate([90,0,90])
    side();

    translate([1+(fax/2),-1-fay/2,-1])
    rotate([90,0,90])
    side();

    difference(){
        face();
        translate([-fhx/2,-fhy/2,-10])
        oledholes();
    }
}

module zeroframe(){
    difference(){
        cube([mhx+8,mhy+8,3]);
        union(){
            translate([4,4,-2])
            zeroholes();
            translate([6,6,-2])
            cube([mhx-4,mhy-4,6]);
        }
    }
    translate([((mhx+8)/2)+(33/2),1,0])
    // translate([0,0.0])
    rotate([90,0,90])
    side();
    // 33
    translate([((mhx+8)/2)-((33/2)+2),1,0])
    rotate([90,0,90])
    side();
}

zeroframe();

rotate([0,180,0])
translate([-mhx/2-4,mhy/2+4,-27])
oledassy();
