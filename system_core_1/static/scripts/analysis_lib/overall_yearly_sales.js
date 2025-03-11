import { yearlySalesAnalysis } from "./yearly_analysis.js";

const urlYearlyOther = '/system_core_1/get_yearly_sales_total/';
const destYearlyOther = '.yearly_sales_chart_total';
const chartTypeYearlyOther = 'bar';
const loaderYearlyOther = '.yearly_sales_chart_loader_total';

yearlySalesAnalysis(
    urlYearlyOther, destYearlyOther,
    chartTypeYearlyOther, loaderYearlyOther,
  );