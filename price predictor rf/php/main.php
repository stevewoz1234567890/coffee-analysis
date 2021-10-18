<?php

require_once __DIR__ . '/load_data.php';
require_once __DIR__ . '/decision_tree.php';
require_once __DIR__ . '/random_forest.php';

function main()
{
    $data_set = load_data(__DIR__ . '/data.txt');
    $count = count($data_set);
    $train_count = floor($count * 0.7);
    $test_count = $count - $train_count;

    shuffle($data_set);
    $training_set = array_slice($data_set, 0, $train_count);
    $test_set = array_slice($data_set, $train_count, $test_count);

    $trees = random_forest_train($training_set, 1600, 5);

    $truth = array_map(
        function ($i) { return $i[27]; },
        $test_set);

    $estimated = array_map(
        function ($i) use ($trees) { return random_forest_classify($trees, $i); },
        $test_set);

    $confusion_matrix = build_confusion_matrix($truth, $estimated);
    foreach ($confusion_matrix as $key => $count) {
        echo "$key,$count\n";
    }

    echo 'accuracy = ' . calc_accuracy($confusion_matrix) . "\n";
}

function build_confusion_matrix($truth, $estimated)
{
    return array_count_values(
        array_map(
            function ($t, $e) { return "$t,$e"; }, $truth, $estimated));
}

function calc_accuracy($confusion_matrix)
{
    $correct = 0;
    foreach ($confusion_matrix as $key => $count) {
        list ($truth, $estimated) = explode(',', $key);
        if ($truth == $estimated) {
            $correct += $count;
        }
    }

    return $correct / array_sum($confusion_matrix);
}

main();
