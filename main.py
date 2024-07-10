import cn.felord.payment.autoconfigure.EnableMobilePay
import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Profile
import org.springframework.core.io.Resource
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import cn.felord.payment.wechat.enumeration.TradeBillType
import cn.felord.payment.wechat.v3.WechatApiProvider
import cn.felord.payment.wechat.v3.WechatDirectPayApi
import cn.felord.payment.wechat.v3.model.*
import com.fasterxml.jackson.databind.node.ObjectNode
import java.time.LocalDate
import java.time.Month

@EnableMobilePay
@Configuration
class PayConfig

@Profile("wechat", "dev")
@RestController
@RequestMapping("/marketing")
class PayController(private val wechatApiProvider: WechatApiProvider) {

    private val TENANT_ID = "mobile"

    @PostMapping("/js")
    fun js(@RequestParam orderId: String): ObjectNode? {
        val payParams = PayParams().apply {
            description = "felord.cn"
            outTradeNo = orderId // Assume this should be the provided orderId
            notifyUrl = "/wxpay/callbacks/transaction"
            amount = Amount().apply { total = 100 }
            payer = Payer().apply { openid = "ooadI5kQYrrCqpgbisvC8bEw_oUc" }
        }
        return wechatApiProvider.directPayApi(TENANT_ID).jsPay(payParams).body
    }

    @GetMapping("/tradebill")
    fun download(): ResponseEntity<Resource> {
        val wechatDirectPayApi = wechatApiProvider.directPayApi(TENANT_ID)
        val tradeBillParams = TradeBillParams().apply {
            billDate = LocalDate.of(2021, Month.MAY, 20)
            billType = TradeBillType.ALL
        }
        return wechatDirectPayApi.downloadTradeBill(tradeBillParams)
    }

    @GetMapping("/fundflowbill")
    fun fundFlowBill(): ResponseEntity<Resource> {
        val wechatDirectPayApi = wechatApiProvider.directPayApi(TENANT_ID)
        val fundFlowBillParams = FundFlowBillParams().apply {
            billDate = LocalDate.of(2021, Month.MAY, 20)
        }
        return wechatDirectPayApi.downloadFundFlowBill(fundFlowBillParams)
    }
}