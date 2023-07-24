import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.apache.fineract.accounting.financialactivityaccount.service.FinancialActivityAccountReadPlatformServiceImpl;
import org.apache.fineract.accounting.financialactivityaccount.data.FinancialActivityAccountData;
import org.apache.fineract.infrastructure.core.service.RoutingDataSource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;

import java.util.List;

import static org.mockito.Mockito.*;

public class FinancialActivityAccountReadPlatformServiceImplTest {

    @InjectMocks
    FinancialActivityAccountReadPlatformServiceImpl financialActivityAccountReadPlatformService;

    @Mock
    JdbcTemplate jdbcTemplate;

    @Mock
    RowMapper<FinancialActivityAccountData> financialActivityAccountMapper;

    @BeforeEach
    public void init() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testRetrieveAll() {
        when(jdbcTemplate.query(anyString(), eq(financialActivityAccountMapper), any())).thenReturn(List.of());
        List<FinancialActivityAccountData> result = financialActivityAccountReadPlatformService.retrieveAll();
        verify(jdbcTemplate, times(1)).query(anyString(), eq(financialActivityAccountMapper), any());
    }

    @Test
    public void testRetrieve_WhenFinancialActivityAccountIdExists() {
        when(jdbcTemplate.queryForObject(anyString(), eq(financialActivityAccountMapper), any())).thenReturn(new FinancialActivityAccountData());
        FinancialActivityAccountData result = financialActivityAccountReadPlatformService.retrieve(1L);
        verify(jdbcTemplate, times(1)).queryForObject(anyString(), eq(financialActivityAccountMapper), any());
    }

    @Test
    public void testRetrieve_WhenFinancialActivityAccountIdDoesNotExist() {
        when(jdbcTemplate.queryForObject(anyString(), eq(financialActivityAccountMapper), any())).thenThrow(new RuntimeException());
        try {
            FinancialActivityAccountData result = financialActivityAccountReadPlatformService.retrieve(1L);
        } catch (RuntimeException e) {
            verify(jdbcTemplate, times(1)).queryForObject(anyString(), eq(financialActivityAccountMapper), any());
        }
    }
}
