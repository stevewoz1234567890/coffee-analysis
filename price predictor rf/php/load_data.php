<?php

function load_data($filename)
{
    $lines = file($filename, FILE_IGNORE_NEW_LINES);

    $data = array();
    foreach ($lines as $l) {
        $data[] = parse_line($l);
    }

    return $data;
}

function parse_line($line)
{
    $data = array();
    $fields = explode(",", $line);

// 'quality_score,Aroma,Flavor,Aftertaste,Acidity,Body,Balance,Uniformity,Clean Cup,Sweetness,Cupper Points,Total Cup Points,Moisture,Category One Defects,Quakers,Category Two Defects,Color_Blue-Green,Color_Bluish-Green,Color_Green,Color_None,Color_Unknown,Processing Method_Natural / Dry,Processing Method_Other,Processing Method_Pulped natural / honey,Processing Method_Semi-washed / Semi-pulped,Processing Method_Unknown,Processing Method_Washed / Wet,Price 
    return array(
        (float) $fields[0],   //        
        (float) $fields[1], // 
        (float) $fields[2], //                 
        (float) $fields[3], //                
        (float) $fields[4], //            
        (float) $fields[5], //       
        (float) $fields[6], //       
        (float) $fields[7], //       
        (float) $fields[8], //       
        (float) $fields[9], //       
        (float) $fields[10], //       
        (float) $fields[11], //       
        (float) $fields[12], //       
        (float) $fields[13], //       
        (float) $fields[14], //       
        (float) $fields[15], //       
        (float) $fields[16], //       
        (float) $fields[17], //       
        (float) $fields[18], //       
        (float) $fields[19], //       
        (float) $fields[20], //       
        (float) $fields[21], //       
        (float) $fields[22], //       
        (float) $fields[23], //       
        (float) $fields[24], //       
        (float) $fields[25], //       
        (float) $fields[26], //       
        (float) $fields[27], //      
    );
}
