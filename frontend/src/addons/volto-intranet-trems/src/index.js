import AreaView from './components/View/AreaView';
import { cloneDeep } from 'lodash';
// Blocos
import ClimaEdit from './components/Blocks/Clima/Edit';
import ClimaView from './components/Blocks/Clima/View';
// Icones
import climaSVG from '@plone/volto/icons/cloud.svg';
// reducers
import { climaData } from './reducers/climaData';

const applyConfig = (config) => {
  config.settings = {
    ...config.settings,
    isMultilingual: false,
    supportedLanguages: ['pt-br'],
    defaultLanguage: 'pt-br',
  };
  config.views.contentTypesViews = {
    ...config.views.contentTypesViews,
    Area: AreaView,
  };
  // Blocos
  config.blocks.blocksConfig.climaBlock = {
    id: 'climaBlock',
    title: 'Clima',
    group: 'common',
    icon: climaSVG,
    view: ClimaView,
    edit: ClimaEdit,
    restricted: false,
    mostUsed: true,
    sidebarTab: 1,
    blockHasOwnFocusManagement: false,
  };

  // Adiciona blocos ao Grid
  const localBlocks = ['climaBlock'];

  // Add Blocks to gridBlock
  // It's important to maintain the chain, and do not introduce pass by reference in
  // the internal `blocksConfig` object, so we clone the object to avoid this.
  ['gridBlock'].forEach((blockId) => {
    const block = config.blocks.blocksConfig[blockId];
    if (
      block !== undefined &&
      block.allowedBlocks !== undefined &&
      block.blocksConfig !== undefined
    ) {
      block.allowedBlocks = [...block.allowedBlocks, ...localBlocks];
      localBlocks.forEach((blockId) => {
        block.blocksConfig[blockId] = cloneDeep(
          config.blocks.blocksConfig[blockId],
        );
      });
    }
  });
  config.addonReducers = {
    ...config.addonReducers,
    climaData,
  };
  return config;
};

export default applyConfig;
