import React from 'react';
import { Database, ShoppingCart, Printer, FileText, AlertCircle, CheckCircle, XCircle } from 'lucide-react';

export default function CashierDiagram() {
  return (
    <div className="w-full h-full bg-gradient-to-br from-blue-50 to-indigo-100 p-8 overflow-auto">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-2 text-indigo-900">
          🛒 Akbar Jaya Cashier System
        </h1>
        <p className="text-center text-gray-600 mb-8">Bug Analysis & System Architecture</p>

        {/* Bug Summary */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4 text-red-600">🐛 Bugs Found Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-red-50 p-4 rounded-lg border-2 border-red-200">
              <div className="flex items-center gap-2 mb-2">
                <XCircle className="text-red-600" size={24} />
                <h3 className="font-bold text-red-800">Critical Bugs: 3</h3>
              </div>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Oversized title (50pt)</li>
                <li>• Oversized cashier (40pt)</li>
                <li>• Missing error handling</li>
              </ul>
            </div>
            <div className="bg-green-50 p-4 rounded-lg border-2 border-green-200">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="text-green-600" size={24} />
                <h3 className="font-bold text-green-800">Fixed: 3</h3>
              </div>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Title: 50pt → 24pt ✓</li>
                <li>• Cashier: 40pt → 16pt ✓</li>
                <li>• Safe data access ✓</li>
              </ul>
            </div>
            <div className="bg-yellow-50 p-4 rounded-lg border-2 border-yellow-200">
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="text-yellow-600" size={24} />
                <h3 className="font-bold text-yellow-800">Warnings: 2</h3>
              </div>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Duplicate code</li>
                <li>• Data inconsistency</li>
              </ul>
            </div>
          </div>
        </div>

        {/* System Architecture */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-6 text-indigo-900">📊 System Architecture</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Program */}
            <div className="bg-indigo-50 p-4 rounded-lg border-2 border-indigo-300">
              <h3 className="font-bold text-lg mb-3 text-indigo-900">main_prog.py</h3>
              <div className="space-y-2 text-sm">
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">User Interface</div>
                  <div className="text-gray-600">PyQt6 GUI components</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Product Display</div>
                  <div className="text-gray-600">Search & browse items</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Shopping Cart</div>
                  <div className="text-gray-600">Add/remove items</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Checkout</div>
                  <div className="text-gray-600">Payment processing</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Stock Manager</div>
                  <div className="text-gray-600">Update inventory</div>
                </div>
              </div>
            </div>

            {/* Receipt Module */}
            <div className="bg-green-50 p-4 rounded-lg border-2 border-green-300">
              <h3 className="font-bold text-lg mb-3 text-green-900">receipt.py</h3>
              <div className="space-y-2 text-sm">
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Receipt Generator</div>
                  <div className="text-gray-600">Format transaction data</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Header Info</div>
                  <div className="text-gray-600">Store, date, cashier</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Item List</div>
                  <div className="text-gray-600">Products × qty × price</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Payment Details</div>
                  <div className="text-gray-600">Total, payment, change</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Terms & Conditions</div>
                  <div className="text-gray-600">Policy text</div>
                </div>
              </div>
            </div>

            {/* Report Module */}
            <div className="bg-purple-50 p-4 rounded-lg border-2 border-purple-300">
              <h3 className="font-bold text-lg mb-3 text-purple-900">report.py</h3>
              <div className="space-y-2 text-sm">
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Date Range Filter</div>
                  <div className="text-gray-600">Select report period</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Sales Analysis</div>
                  <div className="text-gray-600">Aggregate transactions</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Revenue Calculation</div>
                  <div className="text-gray-600">Sum all sales</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">Product Summary</div>
                  <div className="text-gray-600">Qty sold per item</div>
                </div>
                <div className="bg-white p-2 rounded">
                  <div className="font-semibold">PDF Export</div>
                  <div className="text-gray-600">Save report file</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Data Flow */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold mb-6 text-indigo-900">🔄 Data Flow</h2>
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-4">
              <div className="bg-blue-100 p-3 rounded-lg flex-1">
                <Database className="inline mr-2" size={20} />
                <span className="font-semibold">products.csv</span>
                <div className="text-sm text-gray-600 mt-1">
                  Product ID, Name, Category, Price, Stock
                </div>
              </div>
              <div className="text-2xl">→</div>
              <div className="bg-indigo-100 p-3 rounded-lg flex-1">
                <ShoppingCart className="inline mr-2" size={20} />
                <span className="font-semibold">Shopping Cart</span>
                <div className="text-sm text-gray-600 mt-1">
                  Select items, validate stock
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="bg-indigo-100 p-3 rounded-lg flex-1">
                <ShoppingCart className="inline mr-2" size={20} />
                <span className="font-semibold">Checkout</span>
                <div className="text-sm text-gray-600 mt-1">
                  Process payment, reduce stock
                </div>
              </div>
              <div className="text-2xl">→</div>
              <div className="bg-green-100 p-3 rounded-lg flex-1">
                <Printer className="inline mr-2" size={20} />
                <span className="font-semibold">Generate Receipt</span>
                <div className="text-sm text-gray-600 mt-1">
                  Display/print/save as PDF
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="bg-green-100 p-3 rounded-lg flex-1">
                <Printer className="inline mr-2" size={20} />
                <span className="font-semibold">Transaction Data</span>
                <div className="text-sm text-gray-600 mt-1">
                  Customer, cashier, products, datetime
                </div>
              </div>
              <div className="text-2xl">→</div>
              <div className="bg-yellow-100 p-3 rounded-lg flex-1">
                <Database className="inline mr-2" size={20} />
                <span className="font-semibold">sales.csv</span>
                <div className="text-sm text-gray-600 mt-1">
                  Append transaction record
                </div>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="bg-yellow-100 p-3 rounded-lg flex-1">
                <Database className="inline mr-2" size={20} />
                <span className="font-semibold">sales.csv</span>
                <div className="text-sm text-gray-600 mt-1">
                  Historical transaction data
                </div>
              </div>
              <div className="text-2xl">→</div>
              <div className="bg-purple-100 p-3 rounded-lg flex-1">
                <FileText className="inline mr-2" size={20} />
                <span className="font-semibold">Sales Report</span>
                <div className="text-sm text-gray-600 mt-1">
                  Revenue, qty sold, stock analysis
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Code Quality */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold mb-4 text-indigo-900">📈 Code Quality Assessment</h2>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-semibold">Functionality</span>
                <span className="text-green-600">90%</span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div className="bg-green-500 h-3 rounded-full" style={{width: '90%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-semibold">Code Organization</span>
                <span className="text-green-600">80%</span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div className="bg-green-500 h-3 rounded-full" style={{width: '80%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-semibold">Error Handling</span>
                <span className="text-yellow-600">60%</span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div className="bg-yellow-500 h-3 rounded-full" style={{width: '60%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-semibold">User Interface</span>
                <span className="text-yellow-600">65%</span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div className="bg-yellow-500 h-3 rounded-full" style={{width: '65%'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="font-semibold">Scalability</span>
                <span className="text-red-600">50%</span>
              </div>
              <div className="bg-gray-200 rounded-full h-3">
                <div className="bg-red-500 h-3 rounded-full" style={{width: '50%'}}></div>
              </div>
            </div>
            <div className="pt-4 border-t-2">
              <div className="flex justify-between mb-1">
                <span className="font-bold text-lg">Overall Score</span>
                <span className="text-blue-600 font-bold text-lg">7/10</span>
              </div>
              <div className="bg-gray-200 rounded-full h-4">
                <div className="bg-blue-500 h-4 rounded-full" style={{width: '70%'}}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-gray-600 text-sm">
          <p>📄 Full analysis saved to: BUG_ANALYSIS_REPORT.md</p>
          <p>✅ Fixed files: main_prog_FIXED.py, report_FIXED.py</p>
        </div>
      </div>
    </div>
  );
}