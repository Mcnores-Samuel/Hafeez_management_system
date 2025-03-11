import { yearlySalesAnalysisProduct } from "./yearly_analysis.js";

const productAnalysis = '/system_core_1/get_yearly_product_sales/';
const productDest = '.yearly_product_sales_chart';
const productLoader = '.yearly_product_sales_chart_loader';
const chartTypeProduct = 'bar';

yearlySalesAnalysisProduct(
  productAnalysis, productDest,
  chartTypeProduct, productLoader,
);