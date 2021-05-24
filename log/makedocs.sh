#!/bin/sh
pandoc day1.md day2.md day3.md day4.md day5.md day6.md day7.md day8.md \
    day9.md day10.md day11.md day12.md day13.md day14.md day15.md day16.md \
    day17.md day18.md day19.md day20.md day21.md day22.md day23.md day24.md \
    day25.md day26.md -o log.epub \
    --metadata title="Xargon Mapper Development Log" \
    --metadata author="Ryan Armstrong" \
    -f markdown-implicit_figures
pandoc day1.md day2.md day3.md day4.md day5.md day6.md day7.md day8.md \
    day9.md day10.md day11.md day12.md day13.md day14.md day15.md day16.md \
    day17.md day18.md day19.md day20.md day21.md day22.md day23.md day24.md \
    day25.md day26.md -o log.pdf \
    --metadata title="Xargon Mapper Development Log" \
    --metadata author="Ryan Armstrong" \
    --variable geometry="margin=1in" \
    -f markdown-implicit_figures \
    --pdf-engine=lualatex --toc

