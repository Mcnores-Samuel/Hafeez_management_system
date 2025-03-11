import { yearlySalesAnalysis } from "./yearly_analysis.js";

const urlYearly = '/system_core_1/get_yearly_sales/';
const destYearly = '.yearly_sales_chart';
const chartTypeYearly = 'bar';
const loaderYearly = '.yearly_sales_chart_loader';

yearlySalesAnalysis(
  urlYearly, destYearly,
  chartTypeYearly, loaderYearly,
);