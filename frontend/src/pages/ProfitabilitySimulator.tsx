import { useState } from 'react'

interface SimulationParams {
  // Section A: Achat
  listPrice: number
  purchaseNegotiation: number
  notaryFees: number
  buyerAgencyFees: number
  
  // Section B: Travaux
  surface: number
  renovationCostPerM2: number
  contingencyMargin: number
  
  // Section C: Portage
  holdingDurationMonths: number
  monthlyInterest: number
  monthlyCondoCharges: number
  monthlyPropertyTax: number
  
  // Section D: Revente
  targetSalePricePerM2: number
  sellerAgencyFees: number
  saleNegotiation: number
  minProfitMarginPercent: number
}

interface CalculationResults {
  netAcquisitionCost: number
  adjustedWorksCost: number
  totalHoldingCosts: number
  totalCostOfReturn: number
  targetSalePrice: number
  sellerAgencyFeesAmount: number
  netSalePrice: number
  grossMarginEuro: number
  grossMarginPercent: number
  breakEvenPrice: number
  targetMet: boolean
}

export default function ProfitabilitySimulator() {
  const [params, setParams] = useState<SimulationParams>({
    listPrice: 300000,
    purchaseNegotiation: 0.05,
    notaryFees: 0.08,
    buyerAgencyFees: 0.05,
    surface: 100,
    renovationCostPerM2: 500,
    contingencyMargin: 0.1,
    holdingDurationMonths: 6,
    monthlyInterest: 500,
    monthlyCondoCharges: 100,
    monthlyPropertyTax: 50,
    targetSalePricePerM2: 4500,
    sellerAgencyFees: 0.05,
    saleNegotiation: 0.02,
    minProfitMarginPercent: 20,
  })

  const [adText, setAdText] = useState('')
  const [results, setResults] = useState<CalculationResults | null>(null)

  // Fonction de calcul de rentabilité
  const calculateProfitability = (params: SimulationParams): CalculationResults => {
    // Coût d'acquisition net
    const netAcquisitionCost =
      params.listPrice *
      (1 - params.purchaseNegotiation) *
      (1 + params.notaryFees) *
      (1 + params.buyerAgencyFees)

    // Coût des travaux ajusté
    const adjustedWorksCost =
      params.surface *
      params.renovationCostPerM2 *
      (1 + params.contingencyMargin)

    // Frais de portage total
    const totalHoldingCosts =
      params.holdingDurationMonths *
      (params.monthlyInterest +
        params.monthlyCondoCharges +
        params.monthlyPropertyTax)

    // Coût de revient total
    const totalCostOfReturn =
      netAcquisitionCost + adjustedWorksCost + totalHoldingCosts

    // Prix de vente cible
    const targetSalePrice = params.surface * params.targetSalePricePerM2

    // Frais agence revente
    const sellerAgencyFeesAmount = targetSalePrice * params.sellerAgencyFees

    // Prix de vente net après frais
    const netSalePrice =
      targetSalePrice *
      (1 - params.saleNegotiation) -
      sellerAgencyFeesAmount

    // Marge brute (€)
    const grossMarginEuro = netSalePrice - totalCostOfReturn

    // Marge brute (%)
    const grossMarginPercent = (grossMarginEuro / totalCostOfReturn) * 100

    // Seuil de rentabilité
    const breakEvenPrice =
      totalCostOfReturn /
      (1 - params.sellerAgencyFees - params.saleNegotiation)

    // Objectif atteint
    const targetMet = grossMarginPercent >= params.minProfitMarginPercent

    return {
      netAcquisitionCost,
      adjustedWorksCost,
      totalHoldingCosts,
      totalCostOfReturn,
      targetSalePrice,
      sellerAgencyFeesAmount,
      netSalePrice,
      grossMarginEuro,
      grossMarginPercent,
      breakEvenPrice,
      targetMet,
    }
  }

  // Recalculer à chaque changement de paramètre
  const handleParamChange = (key: keyof SimulationParams, value: number) => {
    const newParams = { ...params, [key]: value }
    setParams(newParams)
    setResults(calculateProfitability(newParams))
  }

  // Analyser une annonce (simulation)
  const handleAdAnalysis = () => {
    // Simulation: extraire prix et surface d'une annonce
    const priceMatch = adText.match(/(\d+)\s*€/)
    const surfaceMatch = adText.match(/(\d+)\s*m²/)

    if (priceMatch) {
      const price = parseInt(priceMatch[1])
      handleParamChange('listPrice', price)
    }

    if (surfaceMatch) {
      const surface = parseInt(surfaceMatch[1])
      handleParamChange('surface', surface)
    }
  }

  // Calcul initial
  if (!results) {
    setResults(calculateProfitability(params))
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">
          Simulateur de Rentabilité Achat-Revente
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Colonne Gauche: Paramètres */}
          <div className="lg:col-span-2 space-y-6">
            {/* Section 1: Analyse de l'Annonce */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                📰 Analyse de l'Annonce
              </h2>
              <textarea
                value={adText}
                onChange={(e) => setAdText(e.target.value)}
                placeholder="Collez ici une annonce immobilière..."
                className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
              />
              <button
                onClick={handleAdAnalysis}
                className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-md"
              >
                🤖 Analyser avec l'IA
              </button>
            </div>

            {/* Section 2: Paramètres */}
            <div className="space-y-6">
              {/* Section A: Achat */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  A. Paramètres d'Achat
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Prix Affiché (€)
                    </label>
                    <input
                      type="number"
                      value={params.listPrice}
                      onChange={(e) =>
                        handleParamChange('listPrice', parseFloat(e.target.value))
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Négociation Achat (%)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={params.purchaseNegotiation * 100}
                      onChange={(e) =>
                        handleParamChange(
                          'purchaseNegotiation',
                          parseFloat(e.target.value) / 100
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Frais Notaire (%)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={params.notaryFees * 100}
                      onChange={(e) =>
                        handleParamChange(
                          'notaryFees',
                          parseFloat(e.target.value) / 100
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Frais Agence Achat (%)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={params.buyerAgencyFees * 100}
                      onChange={(e) =>
                        handleParamChange(
                          'buyerAgencyFees',
                          parseFloat(e.target.value) / 100
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
              </div>

              {/* Section B: Travaux */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  B. Paramètres de Travaux
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Surface (m²)
                    </label>
                    <input
                      type="number"
                      value={params.surface}
                      onChange={(e) =>
                        handleParamChange('surface', parseFloat(e.target.value))
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Coût Rénovation (€/m²)
                    </label>
                    <input
                      type="number"
                      value={params.renovationCostPerM2}
                      onChange={(e) =>
                        handleParamChange(
                          'renovationCostPerM2',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Marge Imprévus (%)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={params.contingencyMargin * 100}
                      onChange={(e) =>
                        handleParamChange(
                          'contingencyMargin',
                          parseFloat(e.target.value) / 100
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
              </div>

              {/* Section C: Portage */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  C. Paramètres de Portage
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Durée (mois)
                    </label>
                    <input
                      type="number"
                      value={params.holdingDurationMonths}
                      onChange={(e) =>
                        handleParamChange(
                          'holdingDurationMonths',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Intérêts Mensuels (€)
                    </label>
                    <input
                      type="number"
                      value={params.monthlyInterest}
                      onChange={(e) =>
                        handleParamChange(
                          'monthlyInterest',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Charges Copro (€/mois)
                    </label>
                    <input
                      type="number"
                      value={params.monthlyCondoCharges}
                      onChange={(e) =>
                        handleParamChange(
                          'monthlyCondoCharges',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Taxe Foncière (€/mois)
                    </label>
                    <input
                      type="number"
                      value={params.monthlyPropertyTax}
                      onChange={(e) =>
                        handleParamChange(
                          'monthlyPropertyTax',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
              </div>

              {/* Section D: Revente */}
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  D. Paramètres de Revente
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Prix Vente Cible (€/m²)
                    </label>
                    <input
                      type="number"
                      value={params.targetSalePricePerM2}
                      onChange={(e) =>
                        handleParamChange(
                          'targetSalePricePerM2',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Frais Agence Revente (%)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={params.sellerAgencyFees * 100}
                      onChange={(e) =>
                        handleParamChange(
                          'sellerAgencyFees',
                          parseFloat(e.target.value) / 100
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Négociation Revente (%)
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={params.saleNegotiation * 100}
                      onChange={(e) =>
                        handleParamChange(
                          'saleNegotiation',
                          parseFloat(e.target.value) / 100
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">
                      Marge Min Cible (%)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={params.minProfitMarginPercent}
                      onChange={(e) =>
                        handleParamChange(
                          'minProfitMarginPercent',
                          parseFloat(e.target.value)
                        )
                      }
                      className="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Colonne Droite: Résultats */}
          {results && (
            <div className="lg:col-span-1">
              <div className="sticky top-8 space-y-6">
                {/* Alerte Rentabilité */}
                <div
                  className={`rounded-lg p-6 ${
                    results.targetMet
                      ? 'bg-emerald-100 text-emerald-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  <h3 className="text-lg font-bold mb-2">
                    {results.targetMet ? '✅ CIBLE ATTEINTE' : '❌ CIBLE NON ATTEINTE'}
                  </h3>
                  <p className="text-sm">
                    {results.targetMet
                      ? `Marge de ${results.grossMarginPercent.toFixed(2)}% >= ${params.minProfitMarginPercent}% 🎉`
                      : `Marge de ${results.grossMarginPercent.toFixed(2)}% < ${params.minProfitMarginPercent}% 😞`}
                  </p>
                </div>

                {/* Marge Brute */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-sm font-medium text-gray-500 mb-2">
                    Marge Brute Potentielle
                  </h3>
                  <div className="text-4xl font-bold text-indigo-600 mb-4">
                    {results.grossMarginEuro.toLocaleString('fr-FR', {
                      style: 'currency',
                      currency: 'EUR',
                    })}
                  </div>
                  <div className="text-2xl font-bold text-indigo-600">
                    {results.grossMarginPercent.toFixed(2)}%
                  </div>
                </div>

                {/* Détails des Coûts */}
                <div className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">
                    Détail des Coûts
                  </h3>
                  <dl className="space-y-3 text-sm">
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Coût Achat Net</dt>
                      <dd className="font-medium">
                        {results.netAcquisitionCost.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Coût Travaux</dt>
                      <dd className="font-medium">
                        {results.adjustedWorksCost.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Frais Portage</dt>
                      <dd className="font-medium">
                        {results.totalHoldingCosts.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="border-t border-gray-300 pt-3 flex justify-between font-bold">
                      <dt>Coût Revient Total</dt>
                      <dd>
                        {results.totalCostOfReturn.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Prix Vente Cible</dt>
                      <dd className="font-medium">
                        {results.targetSalePrice.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Frais Agence Revente</dt>
                      <dd className="font-medium">
                        {results.sellerAgencyFeesAmount.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="border-t border-gray-300 pt-3 flex justify-between font-bold">
                      <dt>Prix Vente Net</dt>
                      <dd>
                        {results.netSalePrice.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Seuil Rentabilité</dt>
                      <dd className="font-medium">
                        {results.breakEvenPrice.toLocaleString('fr-FR', {
                          style: 'currency',
                          currency: 'EUR',
                        })}
                      </dd>
                    </div>
                  </dl>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
