#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from tools.report_parser.report_utils import (
    load_xml_file, parse_test_result,
    save_yaml_file, save_html_file,
    concat_testsuite_data
)
from tools.utils import merge_dicts


def parse_args():
    parser = argparse.ArgumentParser('Test results XML parser')
    parser.add_argument(
        '-r', '--run_name',
        nargs='+',
        choices=['UI_auto_smoke', 'regression_testing', 'ext_api_without_schema',
                 'ext_api_schema_custom', 'ext_api_schema_2_4', 'ext_api_schema_2_3',
                 'ext_api_schema_2_1'],
        help='Test run name'
    )
    parser.add_argument(
        '-f', '--file_out',
        default='html',
        choices=['txt', 'html'],
        help='Output file type'
    )
    return parser.parse_args()


def main():
    args = parse_args()
    test_suite_info = []
    test_case_info = {}
    run_name = ', '.join(args.run_name)
    for testrun_name in args.run_name:
        xml_root = load_xml_file(testrun_name)
        test_suite_data, test_case_data = parse_test_result(xml_root)
        test_case_info = merge_dicts(test_case_info, test_case_data)
        test_suite_info.append(test_suite_data)
    test_suite_data = concat_testsuite_data(test_suite_info)
    if args.file_out == 'txt':
        save_yaml_file(run_name, test_suite_data, test_case_info)
    elif args.file_out == 'html':
        save_html_file(run_name, test_suite_data, test_case_info)


if __name__ == '__main__':
    main()
