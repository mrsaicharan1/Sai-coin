// Saicoin ICO

pragma solidity ^0.4.11;

contract saicoin_ico
{
    //Maximum number of hadcoins for sale
    uint public max_saicoins=1000000;
    
    //Introducing the USD to saicoin conversion rate
    uint public usd_to_saicoins=1000;
    //Introducing total number of saicoins bought by investors
    uint public total_saicoins_bought=0;
    
    //Mapping from investor address to equity in saicoins in USD
    mapping(address => uint) equity_saicoins;
    mapping(address => uint) equity_usd;
    
    //Check if investor can buy saicoins
    modifier can_buy_saicoins(uint usd_invested){
        require(usd_invested*usd_to_saicoins+ total_saicoins_bought <= max_saicoins);
        _;
    }
    
    //getting equity of investor in usd
    function equity_in_saicoins(address investor) external returns (uint){
        return equity_saicoins[investor];
    }
    //getting equity of investor in saicoins
    function equity_in_usd(address investor) external returns (uint){
        return equity_usd[investor];
    }
    //Buying saicoins
    function buy_saicoins(address investor, uint usd_invested) external
    can_buy_saicoins(usd_invested)
    {
        uint saicoins_bought = usd_invested*(usd_to_saicoins);
        equity_saicoins[investor]+= saicoins_bought;
        equity_usd[investor]+=equity_saicoins[investor]/usd_to_saicoins;
        total_saicoins_bought+=saicoins_bought;
        
        
    }
    //Selling saicoins
    
    function sell_saicoins(address investor, uint saicoins_sold) external
    {
        equity_saicoins[investor]-= saicoins_sold;
        equity_usd[investor]+=equity_saicoins[investor]*usd_to_saicoins;
        total_saicoins_bought-=saicoins_sold;
        
        
    }
}
